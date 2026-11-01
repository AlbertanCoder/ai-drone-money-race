"""
Single source of truth for the AI / Drones / AI-Drones projection model.

Consumed by:
  ai_drone_growth.py     -> static PNG poster
  build_dashboard.py     -> interactive HTML dashboard

Units: USD billions of annual investment / spend.
The three series are treated as DISJOINT buckets so they can be stacked:
  AI        = AI spend excluding drone applications
  Drones    = conventional / remote-piloted drone spend, no autonomy
  AI Drones = the intersection (autonomous intelligence in unmanned systems)
"""
import numpy as np

YEARS = np.arange(2000, 2101, 5)

#: Last year on the 5-year grid with any factual grounding, so the dashed
#: fact/projection boundary lands exactly on a real data vertex. Everything
#: after this year is modelled.
HISTORICAL_END = 2025

#: Index into YEARS of the last real data point (2025).
LAST_REAL_IDX = 5

AI = np.array([5, 8, 20, 42, 120, 410, 900, 1600, 2500, 3600, 4900, 6300,
               7600, 8800, 9700, 10400, 10900, 11100, 11200, 11100, 10900], float)

DRONES = np.array([2, 5, 11, 19, 30, 42, 55, 65, 72, 75, 74, 68,
                   60, 50, 40, 30, 22, 16, 11, 8, 6], float)

AI_DRONES = np.array([0.05, 0.2, 0.8, 2.5, 8, 28, 85, 200, 380, 620, 900, 1220,
                      1550, 1860, 2150, 2400, 2600, 2750, 2850, 2900, 2880], float)

#: Illustrative uncertainty fan for the projected segment only.
#: This is NOT a confidence interval. It is a fixed spread that widens linearly
#: with distance from the last real data point, so the chart can show that 2100
#: is far less knowable than 2030 without inventing a statistical model.
#: Width is +/- 60% by 2100 and exactly zero up to LAST_REAL_IDX.
FAN_MAX = 0.60


def _fan(base):
    """Return (lo, hi) arrays that equal *base* historically and widen after it."""
    w = np.zeros_like(base, dtype=float)
    span = float(YEARS[-1] - YEARS[LAST_REAL_IDX])
    for i, y in enumerate(YEARS):
        if y > YEARS[LAST_REAL_IDX]:
            w[i] = FAN_MAX * (y - YEARS[LAST_REAL_IDX]) / span
    return base * (1.0 - w), base * (1.0 + w)


BAND = {k: _fan(v) for k, v in (("ai", AI), ("dr", DRONES), ("aid", AI_DRONES))}

#: (year, is_projected, headline, detail)
#: Verified against primary sources: DARPA Grand Challenge 2005 = 8 Oct 2005 (Stanford
#: "Stanley"); first armed Predator strike = 7 Oct 2001 (CIA, Afghanistan); DJI Phantom
#: announced 7 Jan 2013; FAA Part 107 effective 29 Aug 2016; Nvidia first hit a $1T
#: market cap on 30 May 2023; ChatGPT launched 30 Nov 2022.
EVENTS = [
    (2001, False, "First armed drone strike", "CIA Predator fires a Hellfire in Afghanistan"),
    (2005, False, "DARPA Grand Challenge", "Stanley completes the first autonomous desert drive"),
    (2012, False, "AlexNet wins ImageNet", "Deep-learning inflection point"),
    (2013, False, "DJI Phantom / Prime Air", "Consumer + delivery drones"),
    (2016, False, "AlphaGo / FAA Part 107", "AI milestone, drone rulebook"),
    (2017, False, "Transformer paper", "Foundation-model architecture"),
    (2020, False, "GPT-3 / Bayraktar TB2", "LLM scale; drone war proven"),
    (2022, False, "ChatGPT launches", "Generative AI goes mainstream"),
    (2023, False, "NVIDIA $1T / swarms", "AI capex + combat drone swarms"),
    (2024, False, "Reasoning models", "Test-time compute as a new scaling axis"),
    (2025, False, "AI capex supercycle", "Hyperscaler spend at record levels"),
    (2026, True, "Autonomy-first procurement", "Defence budgets shift to AI drones"),
    (2030, True, "Air-taxi certification", "Autonomous eVTOL at scale"),
    (2034, True, "AI combat aircraft", "First fully AI-piloted fighter"),
    (2040, True, "Autonomy is default", "Non-AI drones fade out"),
    (2045, True, "AI-driven R&D loop", "Recursive AI research cycles"),
    (2050, True, "Orbital drone logistics", "Beyond-atmosphere autonomy"),
    (2060, True, "General-purpose autonomy", "Robotics market matures"),
]

#: Number of events with a verifiable factual basis. Everything flagged True in
#: EVENTS is a forward-looking prediction, not a record of something that happened.
VERIFIED_EVENT_COUNT = sum(1 for e in EVENTS if not e[1])

# ===========================================================================
# Narrative content for the interactive story page.
# Anything marked proj=True is a scenario, not a forecast.
# ===========================================================================

ERAS = [
    {
        "from": 2000, "to": 2009, "proj": False,
        "name": "The Predator Years",
        "lede": ("Drones were a military secret and AI was a punchline. Then two things "
                 "changed quietly: wars needed eyes in the sky, and researchers discovered "
                 "that video-game graphics cards could think."),
        "happened": [
            "Armed Predators fly over Afghanistan and Iraq \u2014 the first combat robots that shoot.",
            "DARPA Grand Challenge: nobody finishes in 2004. Stanford's Stanley finishes in 2005.",
            "Deep belief networks revive neural nets; Google starts its self-driving project in 2009.",
        ],
        "why": [
            "Post-9/11 defence budgets paid for persistent surveillance at almost any price.",
            "GPS, cameras and motion sensors got small, cheap and precise.",
            "GPUs arrived \u2014 vastly more compute for the same money than CPUs.",
        ],
        "bought": "Eyes in the sky, and the first real budgets for machine autonomy.",
        "ai": "$5B \u2192 $20B", "aid": "$50M \u2192 $0.8B",
    },
    {
        "from": 2010, "to": 2015, "proj": False,
        "name": "Deep Learning Wakes Up",
        "lede": ("One competition result in 2012 made a lot of people in tech quietly "
                 "re-plan their decade."),
        "happened": [
            "AlexNet demolishes ImageNet (2012) \u2014 deep learning stops being a curiosity.",
            "DJI ships the Phantom in Jan 2013: a drone anyone can fly straight out of the box.",
            "Amazon announces Prime Air on 60 Minutes in Dec 2013 \u2014 delivery by drone goes public.",
        ],
        "why": [
            "ImageNet handed researchers a huge labelled dataset for free.",
            "Consumer electronics pushed flight controllers, batteries and cameras down in price.",
        ],
        "bought": "Computer vision in every phone, and a consumer drone industry out of nothing.",
        "ai": "$20B \u2192 $42B", "aid": "$0.8B \u2192 $2.5B",
    },
    {
        "from": 2016, "to": 2020, "proj": False,
        "name": "Autonomy Goes Commercial",
        "lede": ("The rules finally caught up with the hardware, and machines started "
                 "doing paid work instead of demos."),
        "happened": [
            "Zipline starts flying blood in Rwanda, Oct 2016 \u2014 the first national drone delivery service.",
            "AlphaGo beats Lee Sedol; the FAA's Part 107 opens US skies to commercial drones.",
            "Transformers (2017) lead to GPT-3 (2020). Bayraktar TB2 rewrites what a cheap drone can do in war.",
        ],
        "why": [
            "Part 107 turned drones from a hobby into a business with a licence.",
            "Foundation models meant one big model could be reused for almost anything.",
        ],
        "bought": "Legality, logistics \u2014 and the blueprint for the 2020s AI boom.",
        "ai": "$42B \u2192 $120B", "aid": "$2.5B \u2192 $8B",
    },
    {
        "from": 2021, "to": 2026, "proj": False,
        "name": "The Capex Supercycle",
        "lede": ("The money stopped being a trickle. This is the chapter you are living "
                 "in right now \u2014 and the one hiring fastest."),
        "happened": [
            "ChatGPT lands Nov 2022 and makes AI a household product; NVIDIA crosses $1T in May 2023.",
            "Ukraine turns cheap FPV drones into a decisive weapon; defence budgets reorganise around autonomy.",
            "Amazon Prime Air reaches 11 sites across 10 US metros and targets ~500 towns by end-2026.",
            "DoorDash, Wing and Wendy's start flying fast food to customers in Christiansburg, VA (Mar 2024).",
        ],
        "why": [
            "Scaling laws held: more compute plus more data kept producing better models.",
            "Cheap inference made it sane to run a model on every single delivery.",
        ],
        "bought": "Datacentres, drone fleets, and a real shortage of people who can build this.",
        "ai": "$120B \u2192 $410B", "aid": "$8B \u2192 $28B",
    },
    {
        "from": 2027, "to": 2040, "proj": True,
        "name": "Autonomy Becomes Default",
        "lede": ("Scenario territory from here. Treat everything from 2027 onward as a "
                 "thought experiment, not a prediction."),
        "happened": [
            "Regulators certify autonomous air taxis and beyond-line-of-sight delivery at scale.",
            "Flying a drone by hand becomes a niche skill, the way driving a manual gearbox did.",
        ],
        "why": [
            "Autonomy gets cheaper per mile every year, while human labour does not.",
            "Logistics labour shortages make automation the cheaper option, not the fancy one.",
        ],
        "bought": "The crossover where AI drones outspend conventional ones for good.",
        "ai": "$900B \u2192 $2.5T", "aid": "$85B \u2192 $380B",
    },
    {
        "from": 2041, "to": 2100, "proj": True,
        "name": "The Machine Economy",
        "lede": ("Long-horizon speculation. Nobody can forecast this far out \u2014 and this "
                 "chart is no exception."),
        "happened": [
            "General-purpose autonomy spans air, ground and sea as one logistics layer.",
            "Growth slows not because demand stops, but because the build-out finishes.",
        ],
        "why": [
            "Every infrastructure market plateaus once penetration saturates.",
            "Spending shifts from building to maintaining, replacing and upgrading.",
        ],
        "bought": "Maintenance and upgrade cycles instead of greenfield growth.",
        "ai": "$2.5T \u2192 $10.9T", "aid": "$380B \u2192 $2.9T",
    },
]


#: Real-world uses. "since" is when the use case reached actual service; a few are
#: approximate and marked approx=True rather than presented as exact dates.
USECASES = [
    {"sector": "Delivery", "name": "Amazon Prime Air", "emoji": "\U0001F4E6",
     "since": "Announced Dec 2013 \u00b7 first commercial 2022", "approx": False,
     "blurb": "Groceries, electronics and medication dropped at your door in as fast as "
              "30 minutes by a fully electric drone.",
     "fact": "11 sites across 10 US metros today \u2014 and Amazon is targeting nearly 500 "
             "cities and towns by the end of 2026."},
    {"sector": "Delivery", "name": "DoorDash \u00d7 Wing \u00d7 Wendy's", "emoji": "\U0001F35F",
     "since": "March 2024", "approx": False,
     "blurb": "A burger and fries flown to the doorstep, ordered through the same app you "
              "already use for takeaway.",
     "fact": "Launched in Christiansburg, Virginia \u2014 among the first US on-demand "
             "restaurant deliveries by a major delivery platform."},
    {"sector": "Delivery", "name": "Walmart \u00d7 Wing", "emoji": "\U0001F6D2",
     "since": "Since ~2023", "approx": True,
     "blurb": "Store-to-door flights in the Dallas\u2013Fort Worth area, launched from the "
              "car park of a store you could walk into.",
     "fact": "Retailers use drones as a third lane next to vans and drivers \u2014 it wins on "
             "the last 10 minutes, not the last 10 miles."},
    {"sector": "Delivery", "name": "Uber Eats \u00d7 Flytrex", "emoji": "\U0001F32E",
     "since": "Announced Sept 2025", "approx": False,
     "blurb": "Uber's first investment in drone delivery: Flytrex's beyond-line-of-sight drones "
              "plugged into the Uber Eats platform, starting in US pilot markets.",
     "fact": "Uber and Flytrex announced the partnership on 18 September 2025. Flytrex has flown "
             "over 200,000 US deliveries and is one of four FAA-approved BVLOS operators."},
    {"sector": "Delivery", "name": "Meituan", "emoji": "\U0001F961",
     "since": "Since ~2021", "approx": True,
     "blurb": "Meal delivery drones over Shenzhen \u2014 the same idea, at Chinese city scale.",
     "fact": "China's delivery platforms fly routes over dense urban blocks where a scooter "
             "is stuck in traffic."},
    {"sector": "Health", "name": "Zipline", "emoji": "\U0001FA78",
     "since": "October 2016", "approx": False,
     "blurb": "Blood, vaccines and medicine parachuted into clinics that no truck can reach "
              "in time.",
     "fact": "Started as a national service in Rwanda in 2016 and has since flown millions of "
             "autonomous deliveries across Africa and the US."},
    {"sector": "Health", "name": "Matternet", "emoji": "\U0001F9EA",
     "since": "Since ~2017", "approx": True,
     "blurb": "Lab samples flown between Swiss hospitals instead of sitting in a van in traffic.",
     "fact": "Hospitals care about minutes on a test result \u2014 flying samples turned a "
             "half-hour drive into a few minutes of air time."},
    {"sector": "Farming", "name": "DJI Agras sprayers", "emoji": "\U0001F33E",
     "since": "Since ~2015", "approx": True,
     "blurb": "Spraying drones cover a field faster than a crew on foot, using less chemical.",
     "fact": "Agriculture is the quiet giant: precision spraying, mapping and crop health "
             "with almost no media coverage."},
    {"sector": "Defence", "name": "FPV & reconnaissance drones", "emoji": "\U0001F6E1\uFE0F",
     "since": "At scale since 2022", "approx": False,
     "blurb": "Cheap, camera-first drones became the most consequential weapon of a modern war.",
     "fact": "Ukraine showed a few hundred dollars of drone could destroy a multi-million "
             "dollar vehicle \u2014 and defence budgets everywhere re-planned around that."},
    {"sector": "Cities", "name": "Waymo robotaxis", "emoji": "\U0001F695",
     "since": "Public since ~2020", "approx": True,
     "blurb": "Ground autonomy: cars with nobody in the driver's seat, on public streets.",
     "fact": "The same perception-and-decide stack that flies a drone drives a taxi \u2014 the "
             "skills transfer between them."},
    {"sector": "Industry", "name": "Inspection drones", "emoji": "\U0001F3D7\uFE0F",
     "since": "Since ~2015", "approx": True,
     "blurb": "Bridges, wind turbines and power lines checked without scaffolding or rope access.",
     "fact": "The boring, profitable core of the industry: it replaces a dangerous job, so "
             "companies pay quickly."},
    {"sector": "Rescue", "name": "Thermal search & rescue", "emoji": "\U0001F525",
     "since": "Since ~2018", "approx": True,
     "blurb": "Thermal cameras find people in the dark and spot wildfire hotspots before crews arrive.",
     "fact": "One of the few areas where the drone is unambiguously the good guy \u2014 and "
             "municipal budgets now line-item for it."},
    {"sector": "Play", "name": "Cinema & FPV racing", "emoji": "\U0001F3AC",
     "since": "Since ~2013", "approx": True,
     "blurb": "Cinematic aerials in almost every advert, plus drone racing as a spectator sport.",
     "fact": "An entire creative industry built on a toy that got good \u2014 and a common "
             "way people first meet the technology."},
]


#: Roles in the autonomy economy.
#: `demand` and `pay` are EDITORIAL 1-5 ratings, not surveyed salary data.
CAREERS = [
    {"role": "Drone pilot & flight ops", "emoji": "\U0001F3AE", "demand": 4, "pay": 3,
     "blurb": "You fly the missions, plan routes and keep the aircraft legal.",
     "skills": ["FAA Part 107 licence", "Airspace & weather", "Risk assessment", "Flight logging"],
     "path": "Part 107 exam \u2192 build flight hours \u2192 ops or dispatch role at a delivery, survey or media company.",
     "tags": ["hands-on", "entry-friendly"]},
    {"role": "Autonomy / robotics engineer", "emoji": "\U0001F916", "demand": 5, "pay": 5,
     "blurb": "You write the software that decides where the aircraft goes next.",
     "skills": ["Python & C++", "ROS 2", "SLAM & path planning", "Control theory"],
     "path": "CS or mechatronics degree \u2192 contribute to PX4 or ArduPilot \u2192 autonomy team.",
     "tags": ["engineering", "deep-tech"]},
    {"role": "Computer vision engineer", "emoji": "\U0001F441\uFE0F", "demand": 5, "pay": 5,
     "blurb": "You teach the machine to see obstacles, people and safe landing spots.",
     "skills": ["PyTorch", "Detection & segmentation", "Dataset engineering", "Edge inference"],
     "path": "Two or three real CV projects in public \u2192 open-source work \u2192 ML engineer.",
     "tags": ["engineering", "deep-tech", "ai"]},
    {"role": "Field technician", "emoji": "\U0001F527", "demand": 4, "pay": 3,
     "blurb": "Every fleet needs someone who can fix a cracked arm at 6am.",
     "skills": ["Electronics & soldering", "Battery safety", "Diagnostics", "Component repair"],
     "path": "Technical diploma or apprenticeship \u2192 manufacturer training (DJI, Skydio, Wing).",
     "tags": ["hands-on", "entry-friendly"]},
    {"role": "Airspace & safety analyst", "emoji": "\U0001F4CB", "demand": 3, "pay": 4,
     "blurb": "You work out how thousands of drones share the sky without hitting anything.",
     "skills": ["FAA / EASA rules", "BVLOS risk modelling", "SORA method", "GIS"],
     "path": "Aviation or engineering background \u2192 safety and regulatory role.",
     "tags": ["rules", "analytical"]},
    {"role": "Sensor & data engineer", "emoji": "\U0001F50C", "demand": 4, "pay": 5,
     "blurb": "You make a dozen noisy sensors agree on where the drone actually is.",
     "skills": ["Sensor fusion", "Calibration", "Signal processing", "Embedded C++"],
     "path": "EE or ME degree \u2192 perception or embedded team.",
     "tags": ["engineering", "deep-tech"]},
    {"role": "Autonomy product & ops", "emoji": "\U0001F4CA", "demand": 3, "pay": 4,
     "blurb": "You decide where the next delivery site goes \u2014 and whether it makes money.",
     "skills": ["Unit economics", "Logistics", "Vendor management", "Data analysis"],
     "path": "Ops, consulting or supply chain \u2192 programme lead on an autonomy rollout.",
     "tags": ["business", "analytical"]},
]

#: Concrete first moves, cheapest first.
STARTERS = [
    "Get an FAA Part 107 certificate. The knowledge test costs US$175, it is a real licence, "
    "and it proves interest better than a CV line ever will.",
    "Build something small and fly it: a sub-250g FPV quad, or a Raspberry Pi with a camera "
    "on a cheap frame. Broken parts teach faster than tutorials.",
    "Learn Python properly, then ROS 2. Nearly every autonomy stack in the world speaks it.",
    "Do ONE computer-vision project end to end \u2014 collect data, train, deploy, measure \u2014 "
    "and put it on GitHub. One finished beats five started.",
    "Join a model-aircraft or drone-racing club. Airspace rules and stick time are learned "
    "in a field, with other people, not from a video.",
    "Follow the hiring, not the hype: Amazon Prime Air, Zipline, Wing, Skydio, DJI, Waymo "
    "and the defence primes all post entry-level roles.",
]

#: Quiz: [question, [options], correct_index, explanation]
QUIZ = [
    ("Which of these happened first?",
     ["ChatGPT launches", "AlexNet wins ImageNet", "The Transformer paper", "DJI ships the Phantom"],
     1, "AlexNet won ImageNet in 2012. The Phantom followed in 2013, Transformers in 2017 and ChatGPT in 2022."),
    ("What did the FAA's Part 107 rule actually do in 2016?",
     ["Banned hobby drones", "Created a licence for commercial drone flying in the US",
      "Required every drone to be registered by a police station", "Legalised drone delivery of alcohol"],
     1, "Part 107 created the Remote Pilot Certificate \u2014 the moment drones became a business, not just a hobby."),
    ("Why did AI investment really take off after 2012?",
     ["A government mandate", "Cheap GPUs, huge labelled datasets and better algorithms",
      "Electricity got cheaper", "Social media companies demanded it"],
     1, "AlexNet combined GPUs with the ImageNet dataset. The ingredients were compute, data and a better algorithm."),
    ("On the chart, what is the 'AI Drone' crossover around 2027?",
     ["Drones getting more expensive", "AI-enabled drones outspending conventional ones",
      "AI stopping being used in drones", "Drones replacing passenger planes"],
     1, "It is the moment autonomous drones overtake non-autonomous ones in spend \u2014 autonomy stops being an add-on and becomes the default."),
    ("Which of these is NOT a real drone delivery use case in service today?",
     ["Blood deliveries in Rwanda", "Fast food in Virginia", "Groceries in Texas",
      "Passenger flights to the Moon"],
     3, "Everything except the Moon flight is running in production right now. The other three are documented on this page."),
]


# ===========================================================================
# ALBERTA VIEW
# ---------------------------------------------------------------------------
# The EVENT DATES below are verified against primary sources (Amii, Transport
# Canada/CNW, PrairiesCan, ACM, Invest Alberta). The $ VALUES are illustrative
# estimates of Alberta-attributed spend, NOT sourced statistics - Alberta does
# not publish a series in these three categories.
# ===========================================================================

ALBERTA = {
    "label": "Alberta",
    "historical_end": 2026,
    "last_real_idx": 5,
    # Y domain is much smaller than the global chart, so it gets its own scale.
    "y0log": 0.0008, "y1log": 100, "y1lin": 13,
    "yticks_log": [0.001, 0.01, 0.1, 1, 10, 100],
    "yticks_lin": [0, 2, 4, 6, 8, 10, 12],

    "ai": [0.05, 0.08, 0.15, 0.3, 0.6, 1.4, 3.0, 4.5, 6.5, 8.5, 10.0,
           11.0, 11.8, 12.2, 12.5, 12.6, 12.6, 12.5, 12.4, 12.2, 12.0],
    "dr": [0.02, 0.05, 0.09, 0.15, 0.22, 0.35, 0.5, 0.65, 0.75, 0.8, 0.8,
           0.75, 0.68, 0.6, 0.5, 0.42, 0.34, 0.27, 0.21, 0.16, 0.12],
    "aid": [0.001, 0.004, 0.01, 0.03, 0.09, 0.25, 0.6, 1.0, 1.5, 2.0, 2.6,
            3.1, 3.5, 3.8, 4.0, 4.1, 4.2, 4.2, 4.1, 4.0, 3.9],

    "events": [
        (2002, False, "Amii founded in Edmonton",
         "Starts as the Alberta Ingenuity Centre for Machine Learning, inside UAlberta computing science."),
        (2003, False, "Richard Sutton joins UAlberta",
         "The co-author of the 1998 RL textbook moves to Edmonton and builds the world's deepest RL group."),
        (2015, False, "Foremost UAS Test Range opens",
         "700+ sq nautical miles of restricted prairie airspace in southern Alberta, seeded with federal money."),
        (2017, False, "DeepMind opens Edmonton office",
         "Google's first AI research office outside the UK; Amii also named a national institute."),
        (2018, False, "First BVLOS pipeline patrol approved",
         "Transport Canada clears Calgary's Canadian UAVs to inspect oil and gas beyond visual line of sight."),
        (2023, False, "DeepMind Edmonton closes",
         "Google shuts the Edmonton office in a round of global cuts \u2014 a hit to the local research cluster."),
        (2025, False, "Sutton & Barto win the Turing Award",
         "The 2024 ACM A.M. Turing Award goes to reinforcement learning \u2014 work done substantially in Edmonton."),
        (2026, False, "Meta commits C$13B to Sturgeon County",
         "A 1 GW data centre campus \u2014 Meta's first in Canada \u2014 announced at the Calgary Stampede."),
        (2030, True, "Alberta compute cluster matures",
         "Scenario: cheap power plus data centres turn the province into an AI-infrastructure exporter."),
        (2035, True, "Autonomous pipeline patrol standard",
         "Scenario: drones fly Alberta's pipeline network as routine infrastructure, not a pilot project."),
        (2040, True, "Autonomous wildfire response",
         "Scenario: detection, mapping and aerial ignition run as one automated loop each fire season."),
        (2050, True, "Autonomy rivals energy services",
         "Scenario: Alberta's autonomy sector becomes a comparable export industry to oilfield services."),
        (2060, True, "Post-energy tech transition",
         "Scenario: the province's main technology export is autonomous industrial systems."),
    ],

    "cards": [
        ("\U0001F9E0", "Amii", "Edmonton", "2002",
         "One of Canada's three national AI institutes. Founded in 2002 as the Alberta Ingenuity "
         "Centre for Machine Learning, out of the UAlberta computing science department.",
         "The reason Edmonton was a global AI city long before AI was a household term."),
        ("\U0001F3C6", "Sutton & Barto \u2014 Turing Award", "Edmonton", "2025",
         "The 2024 ACM A.M. Turing Award, announced 5 March 2025, went to Richard Sutton and "
         "Andrew Barto for reinforcement learning.",
         "Sutton's group at UAlberta and Amii is the closest thing the field has to a founding school."),
        ("\U0001F3E2", "Google DeepMind Edmonton", "Edmonton", "2017\u20132023",
         "Opened July 2017 as DeepMind's first research office outside the UK. Closed in "
         "January 2023 during a round of global layoffs.",
         "Proof a research cluster can attract a hyperscaler \u2014 and that the decision can be reversed."),
        ("\U0001F6E9\uFE0F", "Foremost UAS Test Range", "Foremost", "2015",
         "More than 700 square nautical miles of restricted airspace \u2014 described by its own "
         "backers as one of only two places in Canada where BVLOS testing can happen. Over $1.1M "
         "federal funding since 2015.",
         "Alberta's single biggest physical asset in civilian drone testing."),
        ("\U0001F6E2\uFE0F", "Canadian UAVs", "Calgary", "2018",
         "On 12 June 2018 Transport Canada approved it to inspect remote oil and gas assets beyond "
         "visual line of sight in Canadian civil airspace \u2014 a national first.",
         "BVLOS is the whole ballgame for industrial drones, and an Alberta company got there first."),
        ("\U0001F3D7\uFE0F", "Meta data centre", "Sturgeon County", "2026",
         "More than C$13 billion for a 1 GW campus, Meta's first in Canada, announced July 2026. "
         "Capital Power signed on for 250 MW of supply.",
         "Alberta's pitch is simple: cheap, reliable power and available land for AI compute."),
        ("\U0001F6AB", "Drones vs wildfire aircraft", "Province-wide", "in force",
         "Alberta Wildfire restricts airspace to roughly a 9.26 km (5 nautical mile) radius around "
         "a fire, up to 3,000 ft. Flying a drone there can halt aerial firefighting, with fines up "
         "to $15,000.",
         "The province treats drones as an interference risk in wildfire response, not a tool."),
        ("\U0001F33E", "Prairie agriculture", "Southern Alberta", "emerging",
         "Crop scouting, field mapping and variable-rate spraying are being trialled across some "
         "of the largest farms in Canada; applying pesticide by drone is still tightly regulated.",
         "Low margins plus huge acreage is exactly where drone economics work."),
    ],

    "careers": [
        ("Amii / UAlberta", "Research and applied ML \u2014 one of the deepest reinforcement-learning "
                            "research clusters in the world."),
        ("UCalgary / NAIT / SAIT", "Engineering and applied research \u2014 a large share of the "
                                   "province's technical hires."),
        ("Canadian UAVs, AERIUM & survey firms", "BVLOS operations, inspection and geomatics work."),
        ("Meta and the data-centre build-out", "Power engineering, construction, network operations "
                                               "and facilities at hyperscale."),
        ("Energy majors", "Autonomy and sensing teams for pipelines, methane detection and "
                          "emissions reporting."),
    ],
}

