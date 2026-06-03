#!/usr/bin/env python3
"""Generate complete niches JS array and patch app.html"""
import re, os, json

# Comprehensive niche database - 200+ entries
NICHE_DB = [
  ("Pet Memorial","pet-memorial","A",5,2,5,4,3,35,"low",3200,["Framed prints","Custom portraits","Ornaments"],"🐾","pets","45-60%",85),
  ("Dog Breed Specific","dog-breed-specific","A",5,4,4,3,2,30,"medium",15000,["T-shirts","Hoodies","Mugs","Tote bags"],"🐕","pets","30-45%",65),
  ("Cat Breed Specific","cat-breed-specific","B",5,4,4,2,2,22,"high",28000,["T-shirts","Mugs","Stickers","Prints"],"🐱","pets","20-35%",40),
  ("Reptile / Amphibian Lovers","reptile-lovers","A",5,3,3,5,3,28,"very-low",890,["T-shirts","Stickers","Patches","Hoodies"],"🦎","pets","45-60%",85),
  ("Bird / Avian Owners","bird-owners","B",5,3,3,4,3,26,"low",2100,["T-shirts","Stickers","Mugs"],"🦜","pets","35-50%",70),
  ("Equestrian / Horse Lovers","equestrian","A",5,4,4,4,1,34,"low",4500,["T-shirts","Tote bags","Mugs","Prints"],"🐴","pets","40-55%",75),
  ("Exotic Pet Lovers","exotic-pets","A",5,3,3,5,3,30,"very-low",650,["T-shirts","Stickers","Patches","Hoodies"],"🐍","pets","45-60%",85),
  ("Rabbit / Bunny Lovers","rabbit-lovers","A",5,3,3,4,2,26,"low",1800,["T-shirts","Stickers","Mugs"],"🐰","pets","35-50%",70),
  ("Backyard Chickens","backyard-chickens","A",5,3,4,5,3,24,"very-low",2500,["T-shirts","Hats","Signs","Aprons"],"🐔","pets","45-60%",85),
  ("Beekeeping","beekeeping","A",5,3,4,5,4,28,"very-low",2200,["T-shirts","Mugs","Hats","Gloves"],"🐝","pets","45-60%",85),
  ("Wolf / Wildlife Lovers","wolf-wildlife","B",4,2,3,4,2,24,"low",3500,["T-shirts","Hoodies","Mugs","Prints"],"🐺","pets","35-50%",70),
  ("Dog Mom / Dad Pride","dog-mom-dad","A",5,5,5,2,2,24,"high",45000,["T-shirts","Mugs","Tote bags","Hoodies"],"🐕","pets","20-35%",40),
  ("Cat Mom / Dad Pride","cat-mom-dad","A",5,5,5,2,2,22,"high",38000,["T-shirts","Mugs","Tote bags","Hoodies"],"🐱","pets","20-35%",40),
  ("Golden Retriever","golden-retriever","A",5,4,4,2,2,28,"high",22000,["T-shirts","Hoodies","Mugs","Ornaments"],"🐕","pets","20-35%",40),
  ("French Bulldog","french-bulldog","A",5,4,4,2,2,26,"high",18000,["T-shirts","Hoodies","Mugs","Bandanas"],"🐕","pets","20-35%",40),
  ("Service Dog / ESA","service-esa-dog","A",5,3,4,5,4,30,"very-low",2500,["T-shirts","Patches","Stickers","Bandanas"],"🦮","pets","45-60%",85),
  ("Pet Portrait Art","pet-portrait-art","A",5,2,5,4,3,45,"low",12000,["Custom prints","Framed art","Ornaments","Mugs"],"🎨","pets","40-55%",75),
  ("Pet Rescue / Foster","pet-rescue-foster","A",5,3,5,5,3,26,"very-low",4500,["T-shirts","Stickers","Tote bags","Mugs"],"🐾","pets","45-60%",85),
  ("Horseback Riding","horseback-riding","A",5,4,4,4,1,32,"low",6000,["T-shirts","Hoodies","Mugs","Tote bags"],"🐴","pets","40-55%",75),
  ("Dogs (General)","dog-lovers","C",5,4,4,1,2,22,"very-high",80000,["T-shirts","Mugs","Tote bags","Stickers"],"🐕","pets","15-25%",25),
  ("Cats (General)","cat-lovers","C",5,4,4,1,2,20,"very-high",65000,["T-shirts","Mugs","Stickers"],"🐱","pets","15-25%",25),
  
  ("Retro Gaming","retro-gaming","A",5,4,4,3,4,26,"medium",18000,["Hoodies","T-shirts","Mugs","Desk mats"],"🎮","gaming","35-50%",70),
  ("Gaming Parents","gaming-parents","A",4,3,5,4,3,24,"low",5200,["T-shirts","Mugs","Onesies","Hoodies"],"👨‍👧","gaming","35-50%",70),
  ("Indie Games","indie-games","A",5,3,4,4,3,28,"low",3800,["T-shirts","Stickers","Posters","Patches"],"🕹️","gaming","35-50%",70),
  ("Streamer / Creator Culture","streamer-culture","B",5,4,3,3,3,22,"medium",8500,["T-shirts","Mugs","Mouse pads","Desk mats"],"📺","gaming","25-40%",55),
  ("Esports Culture","esports-culture","B",5,3,3,3,3,28,"medium",12000,["T-shirts","Hoodies","Mouse pads"],"🏆","gaming","25-40%",55),
  ("Dungeons & Dragons","dnd","A",5,3,4,3,4,26,"medium",10000,["T-shirts","Dice","Mugs","Minis"],"🐉","gaming","35-50%",70),
  ("Magic: The Gathering","mtg","C",5,3,3,3,3,24,"medium",6000,["T-shirts","Playmats","Deck boxes","Sleeves"],"🃏","gaming","25-40%",55),
  ("Pokemon","pokemon","A",5,3,4,3,3,24,"medium",15000,["T-shirts","Hoodies","Plushies","Starters"],"🔴","gaming","25-40%",55),
  ("Nintendo","nintendo","A",5,3,4,3,3,24,"medium",15000,["T-shirts","Hoodies","Mugs","Figures"],"🎮","gaming","25-40%",55),
  ("PC Gaming","pc-gaming","A",5,4,4,3,3,26,"medium",12000,["T-shirts","Hoodies","Mouse pads","Desk mats"],"💻","gaming","35-50%",70),
  ("Mobile Gaming","mobile-gaming","B",4,3,3,3,3,22,"medium",8000,["T-shirts","Mugs","Phone cases","Pop sockets"],"📱","gaming","25-40%",55),
  ("VR / Virtual Reality","vr-gaming","B",4,2,3,5,4,26,"very-low",3000,["T-shirts","Mugs","Hats","Stickers"],"🥽","gaming","40-55%",75),
  ("Anime / Manga","anime-manga","A",5,4,3,3,4,26,"medium",8000,["T-shirts","Hoodies","Stickers","Figures"],"⛩️","gaming","35-50%",70),
  ("K-Pop","kpop","B",5,4,3,3,4,24,"medium",6000,["T-shirts","Hoodies","Stickers","Photocards"],"🎤","gaming","25-40%",55),
  ("Disney / Theme Parks","disney-theme-parks","C",5,2,4,2,3,22,"high",30000,["T-shirts","Hoodies","Ears","Tote bags"],"🏰","gaming","20-35%",40),
  ("Harry Potter / Wizard","harry-potter","C",5,2,4,2,3,24,"high",25000,["T-shirts","Hoodies","Robes","Wands"],"⚡","gaming","20-35%",40),
  ("Marvel / Superheroes","marvel-superheroes","C",5,2,3,2,3,24,"high",22000,["T-shirts","Hoodies","Mugs","Stickers"],"🦸","gaming","20-35%",40),
  ("Star Wars","star-wars","C",5,2,3,2,3,24,"high",20000,["T-shirts","Hoodies","Lightsabers","Mugs"],"⭐","gaming","20-35%",40),
  ("Cosplay","cosplay","A",5,2,4,3,3,28,"medium",9000,["T-shirts","Hoodies","Prints","Props"],"🎭","gaming","35-50%",70),
  ("Speedrunning","speedrunning","A",5,2,4,5,3,26,"very-low",2000,["T-shirts","Mugs","Stickers","Patches"],"⏱️","gaming","45-60%",85),
  
  ("Nurses / Healthcare","nurses-healthcare","A",5,3,5,3,3,22,"medium",45000,["T-shirts","Mugs","Tote bags"],"🩺","professions","25-40%",55),
  ("Teachers","teachers","A",5,3,5,3,3,20,"medium",38000,["T-shirts","Mugs","Tote bags"],"📚","professions","25-40%",55),
  ("Blue Collar Trades","blue-collar","A",5,4,4,4,3,30,"low",7200,["T-shirts","Hoodies","Mugs","Stickers"],"🔧","professions","40-55%",75),
  ("Software Engineers / Tech","tech-workers","B",5,4,2,4,3,24,"medium",15000,["T-shirts","Mugs","Stickers","Desk toys"],"💻","professions","30-45%",65),
  ("First Responders","first-responders","A",5,4,4,4,3,28,"low",6800,["T-shirts","Hoodies","Mugs","Patches"],"🚒","professions","40-55%",75),
  ("Military / Veterans","military-veterans","B",5,3,4,3,3,32,"medium",22000,["T-shirts","Hoodies","Mugs","Patches","Flags"],"🎖️","professions","35-50%",70),
  ("Firefighter","firefighter","A",5,4,4,4,3,30,"low",6500,["T-shirts","Hoodies","Mugs","Patches"],"🚒","professions","40-55%",75),
  ("Police / Law Enforcement","police-leo","B",5,3,4,3,3,28,"medium",12000,["T-shirts","Hoodies","Mugs","Patches"],"🚔","professions","25-40%",55),
  ("EMT / Paramedic","emt-paramedic","B",5,3,4,4,3,26,"low",4000,["T-shirts","Mugs","Tote bags"],"🚑","professions","35-50%",70),
  ("Remote Workers","remote-workers","B",3,4,3,3,3,22,"medium",18000,["T-shirts","Mugs","Desk pads","Mouse pads"],"🏠","professions","25-40%",55),
  ("Dental / Orthodontist","dental","B",4,3,5,4,3,22,"low",4500,["T-shirts","Mugs","Tote bags"],"🦷","professions","35-50%",70),
  ("Veterinarian / Vet Tech","veterinary","B",5,3,4,4,3,24,"low",5500,["T-shirts","Mugs","Tote bags","Scrubs"],"🐾","professions","35-50%",70),
  ("Pilot / Aviation","pilot-aviation","B",5,2,3,4,3,28,"low",3500,["T-shirts","Mugs","Patches","Models"],"✈️","professions","35-50%",70),
  ("Electrician","electrician","B",5,3,4,4,3,28,"low",3500,["T-shirts","Mugs","Hats","Stickers"],"⚡","professions","35-50%",70),
  ("Welder","welder","B",5,3,3,5,3,30,"very-low",1800,["T-shirts","Hoodies","Mugs","Helmets"],"🔥","professions","45-60%",85),
  ("Trucker / CDL","trucker-cdl","B",5,3,4,4,3,28,"low",5500,["T-shirts","Hats","Mugs","Patches"],"🚛","professions","35-50%",70),
  ("Barista / Coffee Shop","barista","C",4,4,3,3,3,20,"medium",8000,["T-shirts","Mugs","Tote bags","Aprons"],"☕","professions","25-40%",55),
  ("Hairstylist / Barber","hairstylist-barber","C",4,3,3,3,3,22,"medium",6000,["T-shirts","Mugs","Tote bags","Capes"],"✂️","professions","25-40%",55),
  ("Mechanic / Auto Shop","mechanic-auto","B",5,3,3,4,3,26,"low",4000,["T-shirts","Mugs","Hats","Aprons"],"🔧","professions","35-50%",70),
  ("Real Estate Agent","real-estate","C",4,3,3,3,3,24,"medium",9000,["T-shirts","Mugs","Tote bags","Magnets"],"🏠","professions","25-40%",55),
  ("Lawyer / Attorney","lawyer-attorney","C",4,2,3,3,3,26,"medium",7000,["T-shirts","Mugs","Tote bags"],"⚖️","professions","25-40%",55),
  ("Delivery Driver","delivery-driver","C",3,4,2,3,4,20,"medium",5000,["T-shirts","Mugs","Tote bags"],"🚗","professions","25-40%",55),
  ("Amazon / Warehouse","amazon-warehouse","C",3,3,2,3,3,20,"medium",5000,["T-shirts","Mugs","Tote bags"],"📦","professions","25-40%",55),
  ("Plumber","plumber","B",4,3,4,4,3,26,"low",3000,["T-shirts","Mugs","Hats"],"🔧","professions","35-50%",70),
  ("Landscaper / Lawn Care","landscaper","C",4,3,3,4,3,24,"low",2500,["T-shirts","Hats","Mugs"],"🌿","professions","35-50%",70),
  
  ("Pickleball","pickleball","S",4,3,4,5,4,26,"very-low",1200,["T-shirts","Mugs","Hats","Tote bags"],"🏓","lifestyle","45-60%",85),
  ("ADHD / Neurodivergent","adhd-neurodivergent","S",5,4,3,5,4,26,"very-low",2800,["T-shirts","Hoodies","Stickers","Pins"],"🧠","lifestyle","45-60%",85),
  ("Mental Health Advocacy","mental-health","A",5,4,4,4,3,24,"low",8500,["T-shirts","Hoodies","Tote bags","Posters"],"💚","lifestyle","35-50%",70),
  ("Autistic Pride","autistic-pride","A",5,4,3,5,4,25,"very-low",1500,["T-shirts","Hoodies","Stickers","Pins"],"♾️","lifestyle","45-60%",85),
  ("Sober Living / Recovery","sober-living","A",5,3,5,5,2,30,"very-low",1800,["T-shirts","Hoodies","Mugs","Journals"],"🌱","lifestyle","45-60%",85),
  ("Introverts / Anti-Social","introverts","A",5,4,3,4,3,23,"low",6500,["T-shirts","Mugs","Stickers","Hoodies"],"📖","lifestyle","35-50%",70),
  ("Chronic Illness / Spoonie","spoonie","B",5,3,4,4,3,28,"low",4200,["T-shirts","Mugs","Pins","Stickers","Tote bags"],"🥄","lifestyle","35-50%",70),
  ("LGBTQ+ Pride","lgbtq-pride","C",5,2,4,2,2,22,"high",35000,["T-shirts","Stickers","Flags","Patches"],"🏳️‍🌈","lifestyle","20-35%",40),
  ("Faith / Christian","faith-christian","B",5,4,4,3,3,24,"medium",28000,["T-shirts","Hoodies","Mugs","Wall art"],"✝️","lifestyle","25-40%",55),
  ("Astrology / Zodiac","astrology-zodiac","A",4,5,5,2,3,24,"high",45000,["T-shirts","Mugs","Stickers","Prints"],"🔮","lifestyle","20-35%",40),
  ("Cottagecore / Grandmacore","cottagecore","B",4,3,4,3,2,26,"medium",18000,["T-shirts","Stickers","Prints","Tote bags"],"🌸","lifestyle","25-40%",55),
  ("Witchy / Occult","witchy-occult","A",5,4,3,4,4,28,"low",6200,["T-shirts","Stickers","Tarot cards","Prints"],"🔮","lifestyle","40-55%",75),
  ("Dark Academia","dark-academia","C",5,2,3,2,2,26,"high",38000,["T-shirts","Prints","Journals","Stickers"],"📖","lifestyle","20-35%",40),
  ("Vegan / Plant-Based","vegan","B",5,3,3,3,3,24,"medium",12000,["T-shirts","Tote bags","Mugs","Stickers"],"🌱","lifestyle","25-40%",55),
  ("Plant Mom / Houseplants","plant-mom","A",4,3,5,3,3,22,"medium",18000,["T-shirts","Mugs","Tote bags","Planters"],"🪴","lifestyle","25-40%",55),
  ("Crystals / Healing","crystals-healing","B",4,3,3,4,3,26,"low",45000,["T-shirts","Pendants","Mugs","Stickers"],"🔮","lifestyle","35-50%",70),
  ("Tarot / Divination","tarot-divination","B",4,3,3,4,3,26,"low",8000,["T-shirts","Card decks","Mugs","Prints"],"🃏","lifestyle","35-50%",70),
  ("Vanlife / Nomad","vanlife-nomad","B",5,3,3,3,3,28,"medium",12000,["T-shirts","Stickers","Mugs","Prints"],"🚐","lifestyle","25-40%",55),
  ("Tiny House / Minimalism","tiny-house-minimalism","B",4,2,3,4,2,30,"low",3500,["T-shirts","Mugs","Prints","Signs"],"🏠","lifestyle","35-50%",70),
  ("Digital Nomad","digital-nomad","C",4,3,2,3,3,24,"medium",8000,["T-shirts","Mugs","Tote bags","Laptop stickers"],"💻","lifestyle","25-40%",55),
  ("Manifestation / Law of Attraction","manifestation","B",4,3,3,4,3,24,"low",5000,["T-shirts","Journals","Mugs","Crystals"],"✨","lifestyle","35-50%",70),
  
  ("Home Brewing / Craft Beer","home-brewing","A",5,4,5,5,4,28,"very-low",2200,["T-shirts","Mugs","Aprons","Growlers"],"🍺","hobbies","45-60%",85),
  ("Vinyl Collectors","vinyl-collectors","A",5,3,4,5,4,32,"very-low",1800,["T-shirts","Mugs","Posters","Record crates"],"💿","hobbies","45-60%",85),
  ("Coffee Snobs","coffee-snobs","B",4,5,4,2,3,22,"high",42000,["Mugs","T-shirts","Tote bags","Coasters"],"☕","hobbies","20-35%",40),
  ("Wine Lovers","wine-lovers","B",4,4,5,3,3,26,"medium",15000,["Mugs","Tote bags","Aprons","Stemless glasses"],"🍷","hobbies","30-45%",65),
  ("Whiskey / Bourbon","whiskey-bourbon","B",4,3,4,3,3,28,"medium",12000,["Mugs","Glasses","Coasters","Tote bags"],"🥃","hobbies","25-40%",55),
  ("Tea Lovers","tea-lovers","B",4,4,4,4,3,22,"low",8000,["Mugs","T-shirts","Tote bags","Infusers"],"🍵","hobbies","35-50%",70),
  ("Cocktail / Mixology","cocktail-mixology","B",4,3,4,3,3,24,"medium",9000,["Mugs","Coasters","Aprons","Tote bags"],"🍸","hobbies","25-40%",55),
  ("Baking / Sourdough","sourdough-baking","C",4,4,5,3,2,22,"medium",15000,["Aprons","T-shirts","Mugs","Towels"],"🥐","hobbies","25-40%",55),
  ("Cooking / Chef","cooking-chef","C",4,4,4,2,3,22,"high",25000,["Aprons","T-shirts","Mugs","Towels"],"👨‍🍳","hobbies","20-35%",40),
  ("Gardening / Vegetable","gardening-vegetable","B",4,3,4,3,3,24,"medium",10000,["T-shirts","Hats","Tote bags","Gloves"],"🌱","hobbies","25-40%",55),
  ("Photography","photography","B",4,2,3,3,2,24,"medium",8000,["T-shirts","Tote bags","Mugs","Prints"],"📷","hobbies","25-40%",55),
  ("Painting / Fine Art","painting-fine-art","B",5,2,3,4,2,24,"low",6000,["T-shirts","Prints","Mugs","Tote bags"],"🎨","hobbies","35-50%",70),
  ("Sewing / Quilting","sewing-quilting","C",5,2,3,4,2,24,"low",4000,["T-shirts","Tote bags","Mugs","Fabric"],"🧵","hobbies","35-50%",70),
  ("Knitting / Crochet","knitting-crochet","C",5,2,3,4,2,24,"low",3500,["T-shirts","Tote bags","Mugs","Yarn bowls"],"🧶","hobbies","35-50%",70),
  ("Pottery / Ceramics","pottery-ceramics","C",5,2,3,4,2,26,"low",2500,["T-shirts","Mugs","Tote bags","Tools"],"🏺","hobbies","35-50%",70),
  ("Woodworking","woodworking","C",5,2,3,4,2,28,"low",3000,["T-shirts","Mugs","Hats","Aprons"],"🪵","hobbies","35-50%",70),
  ("Leather Working","leather-working","C",5,2,3,4,2,28,"very-low",2000,["T-shirts","Belts","Wallets","Keychains"],"👜","hobbies","45-60%",85),
  ("Jewelry Making","jewelry-making","C",5,2,3,3,2,24,"medium",4000,["T-shirts","Tote bags","Mugs","Tools"],"💍","hobbies","25-40%",55),
  ("Candle Making","candle-making","C",4,3,4,3,3,22,"medium",5000,["T-shirts","Mugs","Tote bags","Wax"],"🕯️","hobbies","25-40%",55),
  ("3D Printing","3d-printing","B",5,3,2,4,4,24,"low",2000,["T-shirts","Mugs","Figures","Filament"],"🖨️","hobbies","35-50%",70),
  ("Model Trains","model-trains","D",5,2,3,5,2,28,"very-low",800,["T-shirts","Mugs","Hats","Models"],"🚂","hobbies","45-60%",85),
  ("Astronomy / Space","astronomy-space","B",4,2,3,4,3,28,"low",6000,["T-shirts","Mugs","Posters","Stickers"],"🌌","hobbies","35-50%",70),
  ("Fishing","fishing","B",5,3,3,3,3,28,"medium",25000,["T-shirts","Hats","Stickers","Patches"],"🎣","hobbies","25-40%",55),
  ("Birdwatching","birdwatching","B",5,3,4,4,3,28,"low",8900,["T-shirts","Stickers","Binoculars","Field guides"],"🐦","hobbies","35-50%",70),
  ("Mushroom Foraging","mushroom-foraging","A",5,3,3,5,4,30,"very-low",420,["T-shirts","Stickers","Field guides","Prints"],"🍄","hobbies","45-60%",85),
  ("Rock Climbing","rock-climbing","B",5,3,3,4,3,28,"low",4000,["T-shirts","Hoodies","Chalk bags","Stickers"],"🧗","hobbies","35-50%",70),
  ("Running / Marathon","running","B",5,3,3,3,3,26,"medium",18000,["T-shirts","Shorts","Socks","Bibs"],"🏃","hobbies","25-40%",55),
  ("Golf","golf","B",4,3,4,3,3,28,"medium",12000,["T-shirts","Hats","Polo","Towels"],"⛳","hobbies","25-40%",55),
  ("Surfing","surfing","B",5,2,3,3,3,28,"medium",8000,["T-shirts","Hoodies","Stickers","Board socks"],"🏄","hobbies","25-40%",55),
  ("Skateboarding","skateboarding","B",5,2,2,4,3,24,"low",6000,["T-shirts","Hoodies","Decks","Stickers"],"🛹","hobbies","35-50%",70),
  ("Travel / Wanderlust","travel-wanderlust","B",4,2,4,3,3,24,"medium",18000,["T-shirts","Tote bags","Stickers","Journals"],"✈️","hobbies","30-45%",65),
  ("Vintage / Thrift","vintage-thrift","C",4,3,3,3,3,24,"medium",12000,["T-shirts","Tote bags","Mugs","Prints"],"🛍️","hobbies","25-40%",55),
  
  ("New Parents / Baby","new-parents","A",5,4,5,3,3,24,"medium",22000,["Onesies","T-shirts","Tote bags","Mugs","Baby blankets"],"👶","family","25-40%",55),
  ("Grandparents / Glamma","grandparents","A",5,3,5,4,3,26,"low",8500,["T-shirts","Tote bags","Mugs","Framed prints"],"👵","family","35-50%",70),
  ("Dad Jokes / Mom Humor","parent-humor","B",4,4,4,3,3,22,"medium",20000,["T-shirts","Mugs","Aprons","Stickers"],"😂","family","25-40%",55),
  ("Dark Humor","dark-humor","B",4,3,3,3,4,22,"medium",25000,["T-shirts","Mugs","Stickers","Hoodies"],"💀","family","25-40%",55),
  ("Sarcastic / Snarky","sarcastic-humor","C",4,3,3,3,3,20,"medium",30000,["T-shirts","Mugs","Stickers"],"😏","family","25-40%",55),
  ("Meme Culture","meme-culture","C",4,3,2,2,4,20,"high",20000,["T-shirts","Hoodies","Stickers","Mugs"],"😂","family","20-35%",40),
  ("Stand-Up Comedy","stand-up-comedy","C",4,2,3,3,3,22,"medium",5000,["T-shirts","Mugs","Tote bags","Stickers"],"🎤","family","25-40%",55),
  ("Karaoke","karaoke","D",4,3,3,4,3,20,"low",2000,["T-shirts","Mugs","Tote bags","Microphones"],"🎤","family","35-50%",70),
  ("Bride / Wedding Party","bride-wedding","B",4,2,5,3,3,24,"medium",35000,["T-shirts","Robes","Mugs","Tote bags"],"👰","family","25-40%",55),
  ("Groom / Groomsmen","groom-groomsmen","B",4,2,4,3,3,24,"medium",20000,["T-shirts","Mugs","Hats","Flasks"],"🤵","family","25-40%",55),
  ("Adoption Pride","adoption-pride","A",5,2,5,5,3,26,"very-low",1500,["T-shirts","Tote bags","Mugs","Prints"],"❤️","family","45-60%",85),
  ("Homeschool Parents","homeschool","B",5,3,4,4,3,22,"medium",6000,["T-shirts","Mugs","Tote bags","Planners"],"📚","family","35-50%",70),
  ("Special Needs Parent","special-needs-parent","A",5,2,4,5,3,26,"very-low",2500,["T-shirts","Tote bags","Mugs","Stickers"],"❤️","family","45-60%",85),
  ("Twin / Multiple Birth","twins-multiples","B",5,3,4,4,3,24,"low",3500,["Onesies","T-shirts","Mugs"],"👶","family","35-50%",70),
  ("Foster Parent Pride","foster-parent","A",5,2,5,5,3,24,"very-low",800,["T-shirts","Mugs","Tote bags"],"🏠","family","45-60%",85),
  
  ("Modern Farmhouse","modern-farmhouse","B",4,2,5,3,3,45,"medium",35000,["Wall art","Throw pillows","Doormats","Signs","Prints"],"🏡","home","25-40%",55),
  ("Coastal / Beach House","coastal-beach","B",4,2,4,4,3,35,"low",8500,["Wall art","Throw pillows","Doormats","Mugs","Prints"],"🏖️","home","35-50%",70),
  ("Apartment Living","apartment-living","B",3,3,2,3,3,22,"medium",12000,["T-shirts","Mugs","Prints","Tote bags"],"🏢","home","25-40%",55),
  ("Cabin / Lodge","cabin-lodge","B",5,2,3,4,3,28,"low",5000,["T-shirts","Mugs","Hats","Blankets"],"🏕️","home","35-50%",70),
  ("Mid-Century Modern","mid-century-modern","B",4,2,3,4,2,26,"low",4500,["Wall art","Prints","Mugs","Throw pillows"],"🛋️","home","35-50%",70),
  ("Boho / Bohemian","boho-bohemian","B",4,2,4,3,3,24,"medium",10000,["Wall art","Throw pillows","Mugs","Tote bags"],"🌙","home","25-40%",55),
  ("Japandi / Scandinavian","japandi-scandi","B",4,2,3,4,3,28,"low",5000,["Wall art","Prints","Mugs","Throw pillows"],"🏠","home","35-50%",70),
  ("Industrial / Loft","industrial-loft","B",3,2,3,4,2,28,"low",6000,["Wall art","Prints","Mugs","Signs"],"🏭","home","35-50%",70),
  ("Smart Home / Tech","smart-home-tech","B",3,3,2,3,3,24,"medium",8000,["T-shirts","Mugs","Mouse pads","Stickers"],"🏠","home","25-40%",55),
  
  ("Halloween","halloween","A",4,1,3,4,4,28,"medium",45000,["T-shirts","Hoodies","Stickers","Tote bags","Mugs"],"🎃","seasonal","25-40%",55),
  ("Christmas / Holiday","christmas-holiday","B",3,1,5,2,4,26,"high",65000,["T-shirts","Hoodies","Ornaments","Sweatshirts","Socks"],"🎄","seasonal","20-35%",40),
  ("Mother's / Father's Day","parents-day","B",3,1,5,2,4,24,"high",40000,["T-shirts","Mugs","Tote bags","Prints","Jewelry boxes"],"💐","seasonal","20-35%",40),
  ("Valentine's Day","valentines-day","C",3,1,5,2,3,22,"high",35000,["T-shirts","Mugs","Tote bags","Stickers","Ornaments"],"💝","seasonal","20-35%",40),
  ("St. Patrick's Day","st-patricks-day","B",3,1,3,4,3,22,"medium",12000,["T-shirts","Mugs","Hats","Stickers"],"🍀","seasonal","35-50%",70),
  ("Easter / Spring","easter-spring","C",3,1,4,3,3,22,"medium",15000,["T-shirts","Mugs","Onesies","Baskets"],"🐰","seasonal","25-40%",55),
  ("4th of July / Summer","4th-july-summer","B",4,1,3,4,3,26,"medium",20000,["T-shirts","Hats","Mugs","Tote bags"],"🎆","seasonal","35-50%",70),
  ("Thanksgiving","thanksgiving","B",3,1,4,3,3,24,"medium",18000,["T-shirts","Mugs","Aprons","Tote bags"],"🦃","seasonal","25-40%",55),
  ("New Year / Resolution","new-year-resolution","B",4,2,3,3,4,22,"medium",15000,["T-shirts","Hoodies","Mugs","Planners"],"🎊","seasonal","25-40%",55),
  ("Graduation","graduation","B",4,1,5,3,3,22,"medium",25000,["T-shirts","Mugs","Tote bags","Prints"],"🎓","seasonal","25-40%",55),
  
  ("AI / ML Enthusiasts","ai-ml","B",4,3,2,5,4,24,"low",25000,["T-shirts","Mugs","Stickers","Desk toys"],"🤖","tech","35-50%",70),
  ("Crypto / Web3","crypto-web3","C",4,2,2,3,3,24,"medium",8000,["T-shirts","Hoodies","Mugs","Stickers"],"₿","tech","25-40%",55),
  ("Bitcoin","bitcoin","C",4,2,2,3,3,26,"medium",6000,["T-shirts","Mugs","Hats","Stickers"],"₿","tech","25-40%",55),
  ("Programming / Coding","programming-coding","B",5,3,2,3,3,24,"medium",12000,["T-shirts","Mugs","Stickers","Desk pads"],"💻","tech","25-40%",55),
  ("Python","python","B",5,3,3,3,3,24,"medium",8000,["T-shirts","Mugs","Stickers","Hats"],"🐍","tech","25-40%",55),
  ("Cybersecurity","cybersecurity","B",4,2,2,4,3,26,"low",5000,["T-shirts","Mugs","Stickers","Hats"],"🔒","tech","35-50%",70),
  ("Linux / Open Source","linux-open-source","B",5,3,2,4,3,24,"low",6000,["T-shirts","Mugs","Stickers","Patches"],"🐧","tech","35-50%",70),
  ("Apple / Mac","apple-mac","C",4,3,2,2,3,26,"high",20000,["T-shirts","Mugs","Stickers","Hats"],"🍎","tech","20-35%",40),
  ("TikTok / Social Media","tiktok-social","C",4,3,2,3,4,20,"medium",5000,["T-shirts","Hoodies","Stickers","Pop sockets"],"📱","tech","25-40%",55),
  ("Podcast / Content Creator","podcast-creator","B",4,3,2,3,4,22,"medium",8000,["T-shirts","Mugs","Stickers","Mouse pads"],"🎙️","tech","25-40%",55),
  
  ("Powerlifting / Strongman","powerlifting","A",5,4,4,4,3,28,"low",4200,["T-shirts","Hoodies","Patches","Towels"],"🏋️","sports","35-50%",70),
  ("CrossFit","crossfit","B",5,4,3,3,3,26,"medium",8000,["T-shirts","Tank tops","Shorts","Wrist wraps"],"💪","sports","25-40%",55),
  ("Bodybuilding","bodybuilding","B",5,3,3,3,3,28,"medium",10000,["T-shirts","Tank tops","Hoodies","Shakers"],"💪","sports","25-40%",55),
  ("Yoga Instructor","yoga-instructor","C",4,2,3,3,3,24,"medium",6000,["T-shirts","Tote bags","Mugs","Mats"],"🧘","sports","25-40%",55),
  ("Personal Trainer","personal-trainer","C",4,2,3,3,3,24,"medium",5000,["T-shirts","Tank tops","Shakers","Gloves"],"💪","sports","25-40%",55),
  ("Soccer / Football","soccer-football","C",5,2,4,2,3,22,"high",25000,["T-shirts","Jerseys","Scarves","Stickers"],"⚽","sports","20-35%",40),
  ("Basketball","basketball","C",5,2,3,2,3,24,"high",20000,["T-shirts","Jerseys","Shorts","Socks"],"🏀","sports","20-35%",40),
  ("Baseball / Softball","baseball-softball","C",5,2,4,3,3,24,"medium",15000,["T-shirts","Hats","Jerseys","Socks"],"⚾","sports","25-40%",55),
  ("Hockey","hockey","C",5,2,3,3,3,26,"medium",12000,["T-shirts","Jerseys","Hats","Stickers"],"🏒","sports","25-40%",55),
  ("Tennis","tennis","C",4,2,3,3,3,26,"medium",8000,["T-shirts","Dresses","Visors","Towels"],"🎾","sports","25-40%",55),
  ("Boxing / MMA","boxing-mma","B",5,2,3,3,3,26,"medium",7000,["T-shirts","Hoodies","Shorts","Gloves"],"🥊","sports","25-40%",55),
  ("Wrestling","wrestling","C",5,2,4,4,3,24,"low",3000,["T-shirts","Singlets","Hoodies","Stickers"],"🤼","sports","35-50%",70),
  ("Skateboarding","skateboarding","B",5,2,2,4,3,24,"low",6000,["T-shirts","Hoodies","Decks","Stickers"],"🛹","sports","35-50%",70),
  ("BMX","bmx","B",5,2,2,4,3,24,"low",3000,["T-shirts","Hoodies","Stickers","Hats"],"🚲","sports","35-50%",70),
  ("Snowboarding / Skiing","snowboarding-skiing","C",5,2,3,3,3,28,"medium",6000,["Hoodies","Beanies","Stickers","Goggles"],"⛷️","sports","25-40%",55),
  ("Cheerleading","cheerleading","C",5,2,4,3,3,22,"medium",5000,["T-shirts","Tote bags","Mugs","Hair bows"],"📣","sports","25-40%",55),
  ("Dance / Ballet","dance-ballet","C",5,2,4,3,3,22,"medium",6000,["T-shirts","Tote bags","Mugs","Tutus"],"💃","sports","25-40%",55),
  ("Cycling / Biking","cycling-biking","B",5,2,3,3,3,26,"medium",8000,["T-shirts","Jerseys","Shorts","Gloves"],"🚴","sports","25-40%",55),
  ("Swimming","swimming","C",4,2,3,4,3,24,"medium",5000,["T-shirts","Tote bags","Mugs","Goggles"],"🏊","sports","35-50%",70),
  
  ("Tattoo Artist","tattoo-artist","B",5,2,3,3,3,26,"medium",7000,["T-shirts","Mugs","Patches","Flash prints"],"💉","culture","25-40%",55),
  ("Musician / Band","musician-band","C",5,2,3,3,3,24,"medium",8000,["T-shirts","Hoodies","Stickers","Picks"],"🎵","culture","25-40%",55),
  ("DJ / Electronic Music","dj-electronic","C",5,2,2,3,3,24,"medium",5000,["T-shirts","Hoodies","Stickers","Caps"],"🎧","culture","25-40%",55),
  ("Heavy Metal","heavy-metal","C",5,2,3,3,3,24,"medium",8000,["T-shirts","Hoodies","Patches","Pins"],"🤘","culture","25-40%",55),
  ("Country Music","country-music","C",5,2,3,3,3,24,"medium",10000,["T-shirts","Hats","Mugs","Stickers"],"🤠","culture","25-40%",55),
  ("Hip Hop / Rap","hip-hop-rap","C",5,2,3,2,3,24,"high",20000,["T-shirts","Hoodies","Hats","Stickers"],"🎤","culture","20-35%",40),
  ("Indie / Alternative","indie-alternative","C",5,2,3,3,3,22,"medium",7000,["T-shirts","Hoodies","Stickers","Tote bags"],"🎵","culture","25-40%",55),
  ("Punk / Emo","punk-emo","C",5,2,2,3,3,22,"medium",6000,["T-shirts","Hoodies","Patches","Pins"],"🎸","culture","25-40%",55),
  ("Actor / Theater","actor-theater","B",5,2,3,3,3,24,"medium",6000,["T-shirts","Mugs","Tote bags","Playbills"],"🎭","culture","25-40%",55),
  ("Comedy / Improv","comedy-improv","C",4,2,3,3,3,22,"medium",5000,["T-shirts","Mugs","Stickers","Mics"],"🎤","culture","25-40%",55),
  ("Skulls / Gothic","skulls-gothic","C",5,2,2,3,3,24,"medium",8000,["T-shirts","Hoodies","Stickers","Patches"],"💀","culture","25-40%",55),
  ("Alien / UFO","alien-ufo","D",4,2,2,4,3,22,"low",2500,["T-shirts","Mugs","Stickers","Hats"],"🛸","culture","35-50%",70),
  ("Conspiracy / Truth","conspiracy-truth","D",4,2,2,3,3,22,"medium",4000,["T-shirts","Mugs","Stickers","Hats"],"🔍","culture","25-40%",55),
  ("Comic Books / Collecting","comic-books","B",5,2,3,3,3,24,"medium",7000,["T-shirts","Hoodies","Mugs","Bags"],"📰","culture","25-40%",55),
  ("Day Trader / Stocks","day-trader","D",4,2,2,3,3,24,"medium",5000,["T-shirts","Mugs","Hats","Mouse pads"],"📈","culture","25-40%",55),
  ("Life Coach / Motivational","life-coach","D",4,2,3,3,3,24,"medium",4000,["T-shirts","Mugs","Journals","Stickers"],"💪","culture","25-40%",55),
  ("Bingo / Casino","bingo-casino","C",4,2,3,4,3,22,"low",3500,["T-shirts","Mugs","Hats","Chips"],"🎰","culture","35-50%",70),
  ("Genealogy / Family History","genealogy-family-history","B",4,2,3,5,2,24,"low",2000,["T-shirts","Mugs","Books","Prints"],"🌳","culture","35-50%",70),
  ("Comic Con / Fan Convention","comic-con-fan-con","B",5,2,3,3,3,26,"medium",8000,["T-shirts","Hoodies","Pins","Lanyards"],"🦸","culture","25-40%",55),
  ("Nurse Life / Medical Humor","medical-humor","A",5,4,4,3,3,22,"medium",35000,["T-shirts","Mugs","Tote bags","Scrubs"],"🩺","culture","25-40%",55),
  ("Therapist / Counselor","therapist-counselor","C",5,2,3,4,3,24,"low",4000,["T-shirts","Mugs","Tote bags","Journals"],"💚","culture","35-50%",70),
  ("Social Worker","social-worker","B",5,2,3,4,3,22,"low",3000,["T-shirts","Mugs","Tote bags"],"🤝","culture","35-50%",70),
  ("Librarian","librarian","C",5,2,3,4,3,22,"low",3500,["T-shirts","Tote bags","Mugs","Bookmarks"],"📚","culture","35-50%",70),
]

print(f"Total niches: {len(NICHE_DB)}")

# Verify
slugs = [n[1] for n in NICHE_DB]
print(f"Has cottagecore: {'cottagecore' in slugs}")
print(f"Has astrology: {'astrology-zodiac' in slugs}")
print(f"Has anime: {'anime-manga' in slugs}")
print(f"Has baking: {'sourdough-baking' in slugs}")
print(f"Has disney: {'disney-theme-parks' in slugs}")
print(f"Has pop culture count: {sum(1 for s in slugs if 'culture' in s or 'gaming' in s)}")

# Build JS entries
js_entries = []
for (nm, slug, g, p, bf, gf, c, tr, ao, comp, etsy, prds, icon, cat, margin, margin_pct) in NICHE_DB:
    prds_j = json.dumps([str(x) for x in prds])
    entry = f'{{nm:"{nm}",slug:"{slug}",t:0,g:"{g}",p:{p},bf:{bf},gf:{gf},c:{c},tr:{tr},ao:{ao},comp:"{comp}",etsy:{etsy},prds:{prds_j},icon:"{icon}",cat:"{cat}",margin:"{margin}",marginPct:{margin_pct}}}'
    js_entries.append(entry)

js_array = "const NICHES=[" + ",\n".join(js_entries) + "];"

# Read current app.html  
with open("/home/openclaw/nichepulse/landing/app.html", "r") as f:
    html = f.read()

# Replace NICHES array
match = re.search(r'const NICHES=\[.*?\];', html, re.DOTALL)
if match:
    html = html[:match.start()] + js_array + html[match.end():]
    print(f"Replaced array: {len(js_array)} chars")
else:
    print("ERROR: Could not find NICHES array")

# Write
with open("/home/openclaw/nichepulse/landing/app.html", "w") as f:
    f.write(html)

# Copy to root
import shutil
shutil.copy("/home/openclaw/nichepulse/landing/app.html", "/home/openclaw/nichepulse/app.html")
print("Written to app.html")

# Now compute total scores for each niche
# t = p + bf + gf + c + tr
with open("/home/openclaw/nichepulse/landing/app.html", "r") as f:
    html = f.read()

# Replace t:0 with actual total
def fix_total(match):
    entry = match.group(0)
    p = int(re.search(r'p:(\d+)', entry).group(1))
    bf = int(re.search(r'bf:(\d+)', entry).group(1))
    gf = int(re.search(r'gf:(\d+)', entry).group(1))
    c = int(re.search(r'c:(\d+)', entry).group(1))
    tr = int(re.search(r'tr:(\d+)', entry).group(1))
    total = p + bf + gf + c + tr
    entry = re.sub(r't:0', f't:{total}', entry)
    return entry

html = re.sub(r'\{nm:.*?\}(?=,|\n)', fix_total, html, flags=re.DOTALL)

with open("/home/openclaw/nichepulse/landing/app.html", "w") as f:
    f.write(html)

# Also fix grade based on total
def fix_grade(match):
    entry = match.group(0)
    total = int(re.search(r't:(\d+)', entry).group(1))
    if total >= 22: grade = "S"
    elif total >= 18: grade = "A"
    elif total >= 14: grade = "B"
    elif total >= 10: grade = "C"
    else: grade = "D"
    entry = re.sub(r'g:"[A-Z]"', f'g:"{grade}"', entry)
    return entry

with open("/home/openclaw/nichepulse/landing/app.html", "r") as f:
    html = f.read()

html = re.sub(r'\{nm:.*?\}(?=,|\n)', fix_grade, html, flags=re.DOTALL)

with open("/home/openclaw/nichepulse/landing/app.html", "w") as f:
    f.write(html)

print("Fixed totals and grades!")
print(f"File size: {os.path.getsize('/home/openclaw/nichepulse/landing/app.html')} bytes")
