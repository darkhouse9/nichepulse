import sys, json
data = json.loads(sys.stdin.read())
p = data.get('product', {})
print('Name:', p.get('name'))
print('Published:', p.get('published'))
print('File info:', p.get('file_info'))
for key in ['files', 'attachments', 'rich_content']:
    val = p.get(key)
    if val:
        print(key + ':', val)
print('')
print('All product keys:')
for k in sorted(p.keys()):
    v = p[k]
    if v and k not in ('description', 'covers'):
        print('  ' + k + ': ' + str(v)[:80])
