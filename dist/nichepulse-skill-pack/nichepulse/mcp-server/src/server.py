"""NichePulse MCP Server — Expose niche scoring via Model Context Protocol."""

import asyncio
import json
import sys
from typing import Any

from nichepulse.scoring import get_niche, list_niches, compare_niches, score_niche


async def handle_request(request: dict) -> dict:
    """Handle MCP JSON-RPC request."""
    method = request.get("method", "")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "tools": [
                    {
                        "name": "score_niche",
                        "description": "Score a niche on 5 dimensions (passion, buy frequency, gift potential, competition, trend)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "Niche name or keyword"},
                                "passion": {"type": "integer", "minimum": 1, "maximum": 5},
                                "buy_frequency": {"type": "integer", "minimum": 1, "maximum": 5},
                                "gift_potential": {"type": "integer", "minimum": 1, "maximum": 5},
                                "competition": {"type": "integer", "minimum": 1, "maximum": 5},
                                "trend": {"type": "integer", "minimum": 1, "maximum": 5},
                            },
                            "required": ["name"],
                        },
                    },
                    {
                        "name": "list_niches",
                        "description": "List pre-scored niches from the database, ranked by score",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "top": {"type": "integer", "default": 10, "description": "Number of results"},
                                "min_score": {"type": "integer", "default": 0},
                            },
                        },
                    },
                    {
                        "name": "compare_niches",
                        "description": "Compare multiple niches side by side",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "keywords": {"type": "array", "items": {"type": "string"}, "description": "Niche keywords to compare"}
                            },
                            "required": ["keywords"],
                        },
                    },
                    {
                        "name": "validate_niche",
                        "description": "Full validation: score + research prompts for a niche idea",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "Niche name or keyword"}
                            },
                            "required": ["name"],
                        },
                    },
                ]
            },
        }

    if method == "tools/call":
        tool = params.get("name", "")
        args = params.get("arguments", {})

        if tool == "score_niche":
            n = score_niche(**{k: v for k, v in args.items() if v is not None})
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps({
                            "name": n.name,
                            "total": n.total,
                            "grade": n.grade,
                            "verdict": n.verdict,
                            "scores": {
                                "passion": n.passion,
                                "buy_frequency": n.buy_frequency,
                                "gift_potential": n.gift_potential,
                                "competition": n.competition,
                                "trend": n.trend,
                            },
                            "margin_estimate": n.margin_estimate,
                            "notes": n.notes,
                        }, indent=2)
                    }]
                },
            }

        if tool == "list_niches":
            top = args.get("top", 10)
            min_score = args.get("min_score", 0)
            niches = list_niches()
            if min_score:
                niches = [n for n in niches if n.total >= min_score]
            results = []
            for n in niches[:top]:
                results.append({
                    "name": n.name,
                    "total": n.total,
                    "grade": n.grade,
                    "margin_estimate": n.margin_estimate,
                })
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {"content": [{"type": "text", "text": json.dumps(results, indent=2)}]},
            }

        if tool == "compare_niches":
            keywords = args.get("keywords", [])
            results = compare_niches(keywords)
            data = [{"name": n.name, "total": n.total, "grade": n.grade} for n in results]
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]},
            }

        if tool == "validate_niche":
            name = args.get("name", "")
            n = get_niche(name)
            if n:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"content": [{"type": "text", "text": json.dumps({
                        "found": True,
                        "name": n.name,
                        "total": n.total,
                        "grade": n.grade,
                        "verdict": n.verdict,
                        "scores": {
                            "passion": n.passion,
                            "buy_frequency": n.buy_frequency,
                            "gift_potential": n.gift_potential,
                            "competition": n.competition,
                            "trend": n.trend,
                        },
                        "next_steps": [
                            f"Search Etsy for '{n.name}' — check competition quality",
                            f"Google Trends: search '{n.name}' — verify 12-month direction",
                            f"Search Reddit r/* for '{n.name}' — check community size",
                            f"Design 10-15 concepts around '{n.name}'",
                        ],
                    }, indent=2)}]},
                }
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {"content": [{"type": "text", "text": json.dumps({
                    "found": False,
                    "message": f"'{name}' not in database. Use score_niche to evaluate it.",
                }, indent=2)}]},
            }

    # Default: error
    return {
        "jsonrpc": "2.0",
        "id": request.get("id"),
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


async def main():
    """Run MCP server over stdio transport."""
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    loop = asyncio.get_event_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    writer_transport, _ = await loop.connect_write_pipe(asyncio.streams.FlowControlMixin, sys.stdout)
    writer = asyncio.StreamWriter(writer_transport, protocol, reader, loop)

    # Signal ready
    sys.stdout.flush()

    while True:
        try:
            line = await reader.readline()
            if not line:
                break
            line = line.decode("utf-8").strip()
            if not line:
                continue
            request = json.loads(line)
            response = await handle_request(request)
            writer.write((json.dumps(response) + "\n").encode("utf-8"))
            await writer.drain()
        except (json.JSONDecodeError, ConnectionError, BrokenPipeError):
            break


if __name__ == '__main__':
    asyncio.run(main())
