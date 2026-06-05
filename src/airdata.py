# Tiered "explore" (flights/globe) destinations per vibe.
# Each place has a minZoom (mz) tier so it surfaces at the right scale:
#   W = world icons (visible on the globe)
#   C = continental / national (appear when you zoom into a continent or country)
#   L = local Bay Area (appear when you zoom into the metro)
# rank within a tier = display priority (1 = top "can't-miss").

W, C, L, N = 0.0, 2.6, 6.4, 5.4

def A(n, lat, lng, mz, rank, r=None):
    return {"n": n, "lat": lat, "lng": lng, "mz": mz, "rank": rank, "r": r or n}

def tier(items, mz):
    return [A(n, la, lo, mz, i + 1) for i, (n, la, lo) in enumerate(items)]

def build(world, na, sa, eu, af, asia, oc, bay, near=()):
    out = tier(world, W)
    for grp in (na, sa, eu, af, asia, oc):
        out += tier(grp, C)
    out += tier(bay, L)
    out += tier(near, N)   # nearby spots that appear when you zoom into a destination
    return out

AIR = {}

AIR["relax"] = build(
    world=[("Maldives",3.2,73.0),("Bali",-8.41,115.19),("Santorini",36.39,25.46),("Bora Bora",-16.5,-151.74),("Amalfi Coast",40.63,14.6)],
    na=[("Big Sur",36.27,-121.81),("Maui",20.79,-156.33),("Sedona",34.87,-111.76),("Lake Tahoe",39.10,-120.03),("Napa Valley",38.50,-122.27),("Aspen",39.19,-106.82),("Banff",51.18,-115.57),("Whistler",50.12,-122.95),("Tulum",20.21,-87.46),("Cabo San Lucas",22.89,-109.91),("Puerto Vallarta",20.65,-105.22),("Palm Springs",33.83,-116.55)],
    sa=[("Rio de Janeiro",-22.91,-43.17),("Patagonia",-50.0,-73.0),("Atacama",-23.85,-67.8),("Iguazu Falls",-25.69,-54.44),("Galápagos",-0.95,-90.97),("Mendoza",-32.89,-68.84),("Cartagena",10.39,-75.51)],
    eu=[("Lake Como",46.0,9.26),("Algarve",37.09,-8.25),("Provence",43.93,5.05),("Mallorca",39.57,2.65),("Hallstatt",47.56,13.65),("Tuscany",43.32,11.33),("Blue Lagoon",63.88,-22.45)],
    af=[("Zanzibar",-6.16,39.2),("Seychelles",-4.68,55.49),("Mauritius",-20.35,57.55),("Marrakech",31.63,-7.99),("Cape Town",-33.92,18.42),("Victoria Falls",-17.92,25.86),("Serengeti",-2.33,34.83)],
    asia=[("Phuket",7.88,98.39),("Kyoto",35.01,135.77),("Ubud",-8.51,115.26),("Goa",15.30,74.12),("Langkawi",6.35,99.80),("Boracay",11.97,121.92),("Hoi An",15.88,108.33)],
    oc=[("Fiji",-17.71,178.07),("Whitsundays",-20.28,148.95),("Queenstown",-45.03,168.66),("Rarotonga",-21.23,-159.78),("Byron Bay",-28.64,153.61),("Lord Howe",-31.55,159.08)],
    bay=[("Half Moon Bay",37.46,-122.43),("Pacifica",37.61,-122.49),("Stinson Beach",37.90,-122.64),("Muir Woods",37.89,-122.57),("Point Reyes",38.07,-122.81),("Sausalito",37.86,-122.49)],
    near=[
        # around Palm Springs
        ("Joshua Tree",33.87,-115.90),("Big Bear Lake",34.24,-116.91),("Idyllwild",33.74,-116.71),("Salton Sea",33.34,-115.83),("Pioneertown",34.16,-116.49),
        # around Sedona
        ("Oak Creek Canyon",34.99,-111.74),("Flagstaff",35.20,-111.65),("Jerome",34.75,-112.11),("Cottonwood",34.74,-112.01),("Slide Rock",34.94,-111.75),
        # around Aspen
        ("Snowmass",39.21,-106.94),("Maroon Bells",39.07,-106.99),("Glenwood Springs",39.55,-107.32),("Crested Butte",38.87,-106.99),("Vail",39.64,-106.37),
        # around Banff
        ("Lake Louise",51.43,-116.18),("Moraine Lake",51.32,-116.18),("Canmore",51.09,-115.36),("Jasper",52.87,-118.08),("Yoho",51.40,-116.49),
        # around Whistler
        ("Squamish",49.70,-123.16),("Garibaldi",49.94,-122.99),("Pemberton",50.32,-122.80),("Joffre Lakes",50.37,-122.50),("Brandywine Falls",50.05,-123.12),
        # around Tulum
        ("Cancún",21.16,-86.85),("Playa del Carmen",20.63,-87.07),("Cozumel",20.42,-86.92),("Akumal",20.40,-87.32),("Bacalar",18.68,-88.39),
        # around Cabo San Lucas
        ("San José del Cabo",23.06,-109.70),("Todos Santos",23.45,-110.22),("La Paz",24.14,-110.31),("Cabo Pulmo",23.44,-109.42),("Loreto",26.01,-111.34),
        # around Puerto Vallarta
        ("Sayulita",20.87,-105.44),("Punta Mita",20.77,-105.51),("Yelapa",20.49,-105.45),("San Pancho",20.92,-105.45),("Bucerías",20.75,-105.33),
        # around Maui
        ("Lahaina",20.88,-156.68),("Hana",20.76,-155.99),("Wailea",20.69,-156.44),("Haleakala",20.71,-156.25),("Kaanapali",20.93,-156.69),
    ],
)

AIR["popular"] = build(
    world=[("Paris",48.86,2.35),("Tokyo",35.68,139.69),("New York",40.71,-74.0),("Rome",41.9,12.5),("Dubai",25.2,55.27)],
    na=[("Las Vegas",36.17,-115.14),("Los Angeles",34.05,-118.24),("San Francisco",37.77,-122.42),("Mexico City",19.43,-99.13),("Cancún",21.16,-86.85),("Toronto",43.65,-79.38),("Chicago",41.88,-87.63)],
    sa=[("Rio de Janeiro",-22.91,-43.17),("Buenos Aires",-34.6,-58.38),("Machu Picchu",-13.16,-72.54),("Cusco",-13.53,-71.97),("Cartagena",10.39,-75.51),("Santiago",-33.45,-70.67),("São Paulo",-23.55,-46.63)],
    eu=[("London",51.51,-0.13),("Barcelona",41.39,2.17),("Amsterdam",52.37,4.90),("Venice",45.44,12.33),("Prague",50.08,14.44),("Istanbul",41.01,28.98),("Athens",37.98,23.73)],
    af=[("Cairo",30.04,31.24),("Marrakech",31.63,-7.99),("Cape Town",-33.92,18.42),("Nairobi",-1.29,36.82),("Giza Pyramids",29.98,31.13),("Victoria Falls",-17.92,25.86),("Zanzibar",-6.16,39.2)],
    asia=[("Bangkok",13.75,100.5),("Singapore",1.35,103.82),("Hong Kong",22.32,114.17),("Bali",-8.41,115.19),("Seoul",37.57,126.98),("Kyoto",35.01,135.77),("Taj Mahal",27.17,78.04)],
    oc=[("Sydney",-33.87,151.21),("Auckland",-36.85,174.76),("Melbourne",-37.81,144.96),("Great Barrier Reef",-18.29,147.7),("Queenstown",-45.03,168.66),("Bora Bora",-16.5,-151.74)],
    bay=[("Golden Gate Bridge",37.82,-122.48),("Alcatraz",37.83,-122.42),("Fisherman's Wharf",37.81,-122.42),("Napa Valley",38.50,-122.27),("Muir Woods",37.89,-122.57)],
)

AIR["unique"] = build(
    world=[("Iceland",64.13,-21.9),("Petra",30.33,35.44),("Machu Picchu",-13.16,-72.54),("Uluru",-25.34,131.04),("Easter Island",-27.11,-109.35)],
    na=[("Antelope Canyon",36.86,-111.37),("Yellowstone",44.43,-110.59),("Death Valley",36.51,-116.93),("White Sands",32.78,-106.17),("Hawaii Volcanoes",19.42,-155.29),("Banff",51.18,-115.57),("Bisbee",31.45,-109.92)],
    sa=[("Salar de Uyuni",-20.13,-67.49),("Galápagos",-0.95,-90.97),("Iguazu Falls",-25.69,-54.44),("Rainbow Mountain",-13.87,-71.30),("Atacama",-23.85,-67.8),("Amazon Manaus",-3.12,-60.02),("Marble Caves",-46.65,-72.62)],
    eu=[("Hallstatt",47.56,13.65),("Giant's Causeway",55.24,-6.51),("Plitvice Lakes",44.88,15.62),("Faroe Islands",62.0,-6.79),("Meteora",39.72,21.63),("Trolltunga",60.12,6.74),("Santorini",36.39,25.46)],
    af=[("Sahara Merzouga",31.10,-4.01),("Socotra",12.46,53.82),("Danakil",14.24,40.30),("Victoria Falls",-17.92,25.86),("Baobab Avenue",-20.25,44.42),("Sossusvlei",-24.73,15.29),("Lake Natron",-2.41,36.07)],
    asia=[("Cappadocia",38.64,34.83),("Zhangjiajie",29.32,110.43),("Halong Bay",20.91,107.18),("Bagan",21.17,94.86),("Pamukkale",37.92,29.12),("Chocolate Hills",9.83,124.14),("Mount Bromo",-7.94,112.95)],
    oc=[("Great Barrier Reef",-18.29,147.7),("Milford Sound",-44.67,167.93),("Pinnacles",-30.60,115.16),("Waitomo Caves",-38.26,175.10),("Lake Hillier",-34.09,123.20),("Moeraki Boulders",-45.35,170.83)],
    bay=[("Mystery Spot",37.02,-122.00),("Glass Beach",39.45,-123.81),("Pinnacles NP",36.49,-121.18),("Winchester House",37.32,-121.95),("Sutro Baths",37.78,-122.51)],
)

AIR["adventure"] = build(
    world=[("Everest",28.0,86.86),("Kilimanjaro",-3.07,37.35),("Patagonia",-50.0,-73.0),("Denali",63.07,-151.0),("Queenstown",-45.03,168.66)],
    na=[("Grand Canyon",36.1,-112.11),("Moab",38.57,-109.55),("Zion",37.30,-113.03),("Yosemite",37.87,-119.54),("Whistler",50.12,-122.95),("Yellowstone",44.43,-110.59),("Arenal Volcano",10.46,-84.70)],
    sa=[("Aconcagua",-32.65,-70.01),("Torres del Paine",-50.94,-73.40),("Inca Trail",-13.30,-72.30),("Amazon",-3.12,-60.02),("Huacachina",-14.09,-75.76),("Cotopaxi",-0.68,-78.44),("Angel Falls",5.97,-62.54)],
    eu=[("Swiss Alps",46.69,7.85),("Chamonix",45.92,6.87),("Dolomites",46.41,11.84),("Norway Fjords",61.10,7.0),("Scottish Highlands",56.82,-5.10),("Tatra Mountains",49.18,20.09),("Pyrenees",42.66,1.0)],
    af=[("Sahara Desert",23.42,12.0),("Atlas Mountains",31.06,-7.92),("Serengeti",-2.33,34.83),("Okavango Delta",-19.28,22.81),("Mount Kenya",-0.15,37.31),("Victoria Falls",-17.92,25.86),("Table Mountain",-33.96,18.40),("Drakensberg",-29.0,29.46),("Fish River Canyon",-27.59,17.66)],
    asia=[("Annapurna",28.6,83.82),("K2",35.88,76.51),("Mount Fuji",35.36,138.73),("Ha Long Bay",20.91,107.18),("Mount Kinabalu",6.08,116.56),("Ladakh",34.15,77.58),("Gobi Desert",43.0,104.0)],
    oc=[("Tongariro",-39.13,175.65),("Blue Mountains",-33.71,150.31),("Cradle Mountain",-41.68,145.95),("Franz Josef Glacier",-43.47,170.18),("Fiordland",-45.42,167.72),("Kokoda Track",-9.0,147.74)],
    bay=[("Mount Tamalpais",37.92,-122.58),("Mount Diablo",37.88,-121.91),("Castle Rock",37.23,-122.10),("Mission Peak",37.51,-121.88),("Marin Headlands",37.83,-122.50)],
)

AIR["golf"] = build(
    world=[("St Andrews",56.34,-2.80),("Pebble Beach",36.57,-121.95),("Augusta",33.50,-82.02),("Dubai",25.06,55.18),("Royal Melbourne",-37.97,145.03)],
    na=[("Pinehurst",35.19,-79.47),("Bandon Dunes",43.18,-124.40),("Torrey Pines",32.90,-117.25),("Whistling Straits",43.85,-87.71),("Cabo del Sol",22.92,-109.81),("TPC Sawgrass",30.20,-81.39),("Bethpage Black",40.74,-73.46)],
    sa=[("Buenos Aires GC",-34.51,-58.49),("Punta del Este",-34.96,-54.95),("Lima GC",-12.05,-77.04),("Santiago GC",-33.45,-70.67),("Rio Olympic",-23.0,-43.41),("São Paulo GC",-23.55,-46.63),("Cartagena GC",10.39,-75.51)],
    eu=[("Valderrama",36.28,-5.28),("Royal County Down",54.22,-5.87),("Le Golf National",48.75,2.08),("Carnoustie",56.50,-2.71),("Sotogrande",36.28,-5.29),("Algarve",37.09,-8.25),("Kingsbarns",56.29,-2.66)],
    af=[("Fancourt",-33.97,22.50),("Leopard Creek",-25.42,31.93),("Gary Player CC",-25.34,27.09),("Durban CC",-29.83,31.01),("Royal Cape",-34.0,18.49),("El Gouna",27.40,33.67),("Marrakech",31.63,-7.99)],
    asia=[("Mission Hills",22.66,114.05),("Sentosa",1.25,103.83),("Kawana",35.02,139.16),("Nine Bridges",33.40,126.61),("Phuket GC",7.88,98.39),("Hua Hin",12.57,99.96),("Haikou",19.95,110.32)],
    oc=[("Kingston Heath",-37.98,145.10),("Cape Kidnappers",-39.64,177.09),("Kauri Cliffs",-34.99,173.73),("Barnbougle",-40.93,147.62),("Tara Iti",-36.18,174.46),("New South Wales GC",-33.99,151.25)],
    bay=[("Olympic Club",37.71,-122.49),("Harding Park",37.72,-122.49),("Presidio GC",37.79,-122.46),("Half Moon Bay Links",37.43,-122.44),("Stanford GC",37.41,-122.18)],
)

AIR["beach"] = build(
    world=[("Maldives",3.2,73.0),("Bora Bora",-16.5,-151.74),("Whitehaven",-20.28,149.04),("Maui",20.79,-156.33),("Seychelles",-4.68,55.49)],
    na=[("Waikiki",21.28,-157.84),("Cancún",21.16,-86.85),("Tulum",20.21,-87.46),("Miami Beach",25.79,-80.13),("Santa Monica",34.01,-118.50),("Cabo San Lucas",22.89,-109.91),("Tofino",49.15,-125.91)],
    sa=[("Copacabana",-22.97,-43.18),("Florianópolis",-27.6,-48.55),("Punta del Este",-34.96,-54.95),("Máncora",-4.10,-81.05),("Cartagena",10.39,-75.51),("Jericoacoara",-2.79,-40.51),("Baía do Sancho",-3.86,-32.44)],
    eu=[("Algarve",37.09,-8.25),("Mallorca",39.57,2.65),("Mykonos",37.45,25.33),("Amalfi",40.63,14.6),("Nice",43.70,7.27),("Costa del Sol",36.51,-4.88),("Zakynthos",37.79,20.75)],
    af=[("Zanzibar",-6.16,39.2),("Mauritius",-20.35,57.55),("Clifton Beach",-33.94,18.38),("Diani Beach",-4.28,39.59),("Sharm el-Sheikh",27.91,34.33),("Tofo",-23.85,35.55),("Anjajavy",-15.18,47.23)],
    asia=[("Phuket",7.88,98.39),("Kuta Bali",-8.72,115.17),("Boracay",11.97,121.92),("Phi Phi",7.74,98.77),("El Nido",11.18,119.41),("Goa",15.30,74.12),("Nha Trang",12.24,109.19)],
    oc=[("Fiji",-17.71,178.07),("Bondi",-33.89,151.27),("Gold Coast",-28.0,153.43),("Rarotonga",-21.23,-159.78),("Lord Howe",-31.55,159.08),("Cable Beach",-17.96,122.21)],
    bay=[("Half Moon Bay",37.46,-122.43),("Stinson Beach",37.90,-122.64),("Baker Beach",37.79,-122.48),("Santa Cruz",36.97,-122.03),("Ocean Beach",37.76,-122.51)],
)

AIR["foodie"] = build(
    world=[("Tokyo",35.68,139.69),("Paris",48.86,2.35),("Lyon",45.76,4.84),("Bangkok",13.75,100.5),("Bologna",44.49,11.34)],
    na=[("New Orleans",29.95,-90.07),("Mexico City",19.43,-99.13),("San Francisco",37.77,-122.42),("New York",40.71,-74.0),("Oaxaca",17.07,-96.72),("Portland",45.52,-122.68),("Montréal",45.50,-73.57)],
    sa=[("Lima",-12.05,-77.04),("Buenos Aires",-34.6,-58.38),("São Paulo",-23.55,-46.63),("Cusco",-13.53,-71.97),("Cartagena",10.39,-75.51),("Bogotá",4.71,-74.07),("Santiago",-33.45,-70.67)],
    eu=[("San Sebastián",43.32,-1.98),("Naples",40.85,14.27),("Barcelona",41.39,2.17),("Florence",43.77,11.26),("Istanbul",41.01,28.98),("Copenhagen",55.68,12.57),("Lisbon",38.72,-9.14)],
    af=[("Marrakech",31.63,-7.99),("Cape Town",-33.92,18.42),("Cairo",30.04,31.24),("Lagos",6.52,3.38),("Addis Ababa",9.03,38.74),("Tunis",36.81,10.18),("Dakar",14.72,-17.47)],
    asia=[("Singapore",1.35,103.82),("Hong Kong",22.32,114.17),("Penang",5.41,100.33),("Seoul",37.57,126.98),("Hanoi",21.03,105.85),("Chengdu",30.57,104.07),("Mumbai",19.08,72.88)],
    oc=[("Melbourne",-37.81,144.96),("Sydney",-33.87,151.21),("Auckland",-36.85,174.76),("Adelaide",-34.93,138.60),("Wellington",-41.29,174.78)],
    bay=[("Napa Valley",38.50,-122.27),("Mission District",37.76,-122.42),("Berkeley",37.87,-122.27),("Healdsburg",38.61,-122.87),("Ferry Building",37.80,-122.39)],
)

AIR["nightlife"] = build(
    world=[("Berlin",52.52,13.40),("Ibiza",38.91,1.43),("Las Vegas",36.17,-115.14),("Bangkok",13.75,100.5),("Rio de Janeiro",-22.97,-43.18)],
    na=[("Miami",25.76,-80.19),("New York",40.71,-74.0),("New Orleans",29.95,-90.07),("Los Angeles",34.05,-118.24),("Montréal",45.50,-73.57),("Cancún",21.16,-86.85),("Tulum",20.21,-87.46)],
    sa=[("Buenos Aires",-34.6,-58.38),("São Paulo",-23.55,-46.63),("Medellín",6.24,-75.58),("Cartagena",10.39,-75.51),("Santiago",-33.45,-70.67),("Lima",-12.05,-77.04),("Florianópolis",-27.6,-48.55)],
    eu=[("Amsterdam",52.37,4.90),("Barcelona",41.39,2.17),("London",51.51,-0.13),("Belgrade",44.82,20.46),("Mykonos",37.45,25.33),("Prague",50.08,14.44),("Tbilisi",41.72,44.79)],
    af=[("Cape Town",-33.92,18.42),("Marrakech",31.63,-7.99),("Lagos",6.52,3.38),("Cairo",30.04,31.24),("Nairobi",-1.29,36.82),("Accra",5.60,-0.19),("Sharm el-Sheikh",27.91,34.33)],
    asia=[("Tokyo",35.68,139.69),("Seoul",37.57,126.98),("Hong Kong",22.32,114.17),("Singapore",1.35,103.82),("Kuta Bali",-8.72,115.17),("Tel Aviv",32.08,34.78),("Goa",15.30,74.12)],
    oc=[("Sydney",-33.87,151.21),("Melbourne",-37.81,144.96),("Gold Coast",-28.0,153.43),("Auckland",-36.85,174.76),("Perth",-31.95,115.86)],
    bay=[("Mission District",37.76,-122.42),("SoMa",37.78,-122.40),("North Beach",37.80,-122.41),("The Castro",37.76,-122.43),("Uptown Oakland",37.81,-122.27)],
)

AIR["culture"] = build(
    world=[("Rome",41.9,12.5),("Kyoto",35.01,135.77),("Cairo",30.04,31.24),("Athens",37.98,23.73),("Cusco",-13.53,-71.97)],
    na=[("Mexico City",19.43,-99.13),("Washington DC",38.91,-77.04),("New York",40.78,-73.96),("Santa Fe",35.69,-105.94),("Québec City",46.81,-71.21),("Chichén Itzá",20.68,-88.57),("Teotihuacán",19.69,-98.84)],
    sa=[("Machu Picchu",-13.16,-72.54),("Cartagena",10.39,-75.51),("Quito",-0.18,-78.47),("La Paz",-16.5,-68.15),("Salvador",-12.97,-38.51),("Easter Island",-27.11,-109.35),("Ouro Preto",-20.39,-43.51)],
    eu=[("Florence",43.77,11.26),("Paris",48.86,2.34),("Vienna",48.21,16.37),("Istanbul",41.01,28.98),("Alhambra",37.18,-3.59),("St Petersburg",59.93,30.34),("Krakow",50.06,19.94)],
    af=[("Giza Pyramids",29.98,31.13),("Marrakech",31.63,-7.99),("Fez",34.04,-5.0),("Lalibela",12.03,39.04),("Timbuktu",16.77,-3.01),("Great Zimbabwe",-20.27,30.93),("Luxor",25.69,32.64)],
    asia=[("Angkor Wat",13.41,103.87),("Varanasi",25.32,82.97),("Forbidden City",39.92,116.39),("Taj Mahal",27.17,78.04),("Jerusalem",31.78,35.22),("Bagan",21.17,94.86),("Xi'an",34.34,108.94)],
    oc=[("Uluru",-25.34,131.04),("Sydney Opera House",-33.86,151.21),("Rotorua",-38.14,176.25),("Waitangi",-35.27,174.09),("Te Papa",-41.29,174.78)],
    bay=[("de Young Museum",37.77,-122.47),("SFMOMA",37.79,-122.40),("Mission Dolores",37.76,-122.43),("Palace of Fine Arts",37.80,-122.45),("UC Berkeley",37.87,-122.26)],
)
