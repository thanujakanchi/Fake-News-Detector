"""
Configuration settings for the Fake News Detection System.
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"

# Ensure directories exist
MODEL_DIR.mkdir(exist_ok=True)

# Model files
MODEL_PATH = MODEL_DIR / "model.pkl"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"

# Dataset paths
DATASET_DIR = BASE_DIR / "dataset"
FAKE_DATASET_PATH = DATASET_DIR / "Fake.csv"
TRUE_DATASET_PATH = DATASET_DIR / "True.csv"

# Model parameters
TFIDF_PARAMS = {
    "stop_words": "english",
    "max_df": 0.7,
    "ngram_range": (1, 2),
    "min_df": 3,
}

CLASSIFIER_PARAMS = {
    "max_iter": 1000,
    "random_state": 42,
    "early_stopping": True,
    "validation_fraction": 0.1,
}

# Training parameters
TEST_SIZE = 0.25
RANDOM_STATE = 42

# Category keywords
CATEGORY_KEYWORDS = {
    "Technology": ["computer", "software", "ai", "technology", "internet", "cyber", "digital", "tech", "algorithm"],
    "Sports": ["cricket", "football", "sports", "match", "player", "coach", "tournament", "athlete", "stadium"],
    "Politics": ["government", "election", "minister", "politics", "president", "senate", "congress", "prime minister"],
    "Business": ["business", "company", "market", "stock", "economy", "finance", "investment", "corporate"],
    "Entertainment": ["movie", "actor", "music", "entertainment", "film", "celebrity", "show", "concert"],
    "Education": ["student", "school", "college", "education", "university", "teacher", "professor", "academic"],
    "Health": ["health", "doctor", "medicine", "hospital", "disease", "treatment", "vaccine", "medical"],
    "Science": ["science", "research", "scientific", "experiment", "discovery", "space", "astronomy", "physics"],
    "Weather": ["weather", "climate", "rain", "storm", "hurricane", "temperature", "forecast"],
    "Travel": ["travel", "tourism", "destination", "hotel", "airline", "tour", "vacation"],
}


# ====== TRUE FACTS ======
KNOWN_TRUE_FACTS = [
    # ===== EARTH & SUN =====
    "earth revolves around the sun",
    "the earth revolves around the sun",
    "earth orbits the sun",
    "the earth orbits the sun",
    "earth rotates around the sun",
    "the earth rotates around the sun",
    "earth goes around the sun",
    "the earth goes around the sun",
    "earth moves around the sun",
    "the earth moves around the sun",
    
    # ===== SCIENCE =====
    "water boils at 100 degrees",
    "water boils at 100 degrees celsius",
    "water freezes at 0 degrees",
    "water freezes at 0 degrees celsius",
    "humans need oxygen",
    "humans need oxygen to survive",
    "the sky is blue",
    "gravity exists",
    "gravity pulls objects down",
    "water is composed of hydrogen and oxygen",
    "photosynthesis produces oxygen",
    "the earth is round",
    "earth is round",
    "the earth is spherical",
    "the sun is a star",
    "the moon orbits the earth",
    "light travels faster than sound",
    "atoms are the building blocks of matter",
    "the human body has 206 bones",
    "the heart pumps blood",
    "the brain controls the body",
    "oxygen is essential for life",
    "carbon dioxide is a greenhouse gas",
    "the sun is the center of our solar system",
    "the earth has one moon",
    "jupiter is the largest planet",
    "pluto is a dwarf planet",
    "the milky way is a galaxy",
    "the universe is expanding",
    "evolution is a scientific theory",
    "dna contains genetic information",
    "cells are the basic unit of life",
    "energy cannot be created or destroyed",
    "e=mc squared",
    "water is h2o",
    "salt is sodium chloride",
    "oxygen makes up 21 percent of the atmosphere",
    "nitrogen makes up 78 percent of the atmosphere",
    "the ozone layer protects us from uv radiation",
    
    # ===== GEOGRAPHY =====
    "india is in asia",
    "china is the most populated country",
    "the pacific ocean is the largest ocean",
    "mount everest is the tallest mountain",
    "the amazon rainforest is the largest rainforest",
    "the sahara desert is the largest hot desert",
    "the nile river is the longest river",
    "the dead sea is the lowest point on earth",
    "the north pole is in the arctic",
    "the south pole is in antarctica",
    "australia is a continent",
    "antarctica is the coldest continent",
    "there are seven continents",
    "asia is the largest continent",
    "russia is the largest country by area",
    "the united states has 50 states",
    "canada has 10 provinces",
    "the himalayas are in asia",
    "the rocky mountains are in north america",
    "the andes mountains are in south america",
    "the great barrier reef is in australia",
    "greenland is the largest island",
    "japan is an island nation",
    "vatican city is the smallest country",
    
    # ===== HISTORY =====
    "world war 1 started in 1914",
    "world war 2 started in 1939",
    "world war 2 ended in 1945",
    "india gained independence in 1947",
    "america gained independence in 1776",
    "the french revolution happened in 1789",
    "the industrial revolution started in england",
    "the renaissance began in italy",
    "the ancient egyptians built pyramids",
    "the great wall of china is in china",
    "the colosseum is in rome",
    "the taj mahal is in india",
    "the pyramids are in egypt",
    "machu picchu is in peru",
    "stonehenge is in england",
    "the roman empire was powerful",
    "alexander the great conquered many lands",
    "genghis khan was a mongol leader",
    "columbus discovered america in 1492",
    "the silk road connected asia and europe",
    "the british empire was the largest empire",
    "napoleon was a french emperor",
    "hitler was a german dictator",
    "gandhi was an indian leader",
    "martin luther king fought for civil rights",
    "nelson mandela fought against apartheid",
    "the cold war was between the us and soviet union",
    "the berlin wall fell in 1989",
    "apollo 11 landed on the moon in 1969",
    "the first airplane was invented by the wright brothers",
    "the telephone was invented by alexander graham bell",
    "the light bulb was invented by thomas edison",
    "the printing press was invented by gutenberg",
    "the computer was invented in the 20th century",
    "the internet was invented in the 20th century",
    
    # ===== BIOLOGY =====
    "humans have 23 pairs of chromosomes",
    "the human body is 60 percent water",
    "the skin is the largest organ",
    "the liver is the largest internal organ",
    "the smallest bone is in the ear",
    "dna is the blueprint of life",
    "genes determine traits",
    "identical twins have the same dna",
    "mammals give birth to live young",
    "whales are mammals",
    "dolphins are mammals",
    "bats are mammals",
    "penguins are birds",
    "snakes are reptiles",
    "frogs are amphibians",
    "fish are vertebrates",
    "insects have six legs",
    "spiders are arachnids",
    "bees are insects",
    "ants are social insects",
    "butterflies undergo metamorphosis",
    "plants need sunlight to grow",
    "plants need water to grow",
    "chlorophyll makes plants green",
    "flowers attract pollinators",
    "bees pollinate flowers",
    "mushrooms are fungi",
    "bacteria are microorganisms",
    "viruses are not living",
    "antibiotics treat bacterial infections",
    "vaccines prevent diseases",
    "penicillin was discovered by alexander fleming",
    
    # ===== ASTRONOMY =====
    "the sun is 93 million miles away",
    "the sun is a yellow dwarf star",
    "the earth is 4.5 billion years old",
    "the universe is 13.8 billion years old",
    "the big bang created the universe",
    "there are 8 planets in our solar system",
    "mercury is the closest planet to the sun",
    "venus is the hottest planet",
    "earth is the third planet from the sun",
    "mars is the red planet",
    "saturn has rings",
    "neptune is the coldest planet",
    "the moon has craters",
    "the moon has no atmosphere",
    "the universe contains billions of galaxies",
    "black holes have strong gravity",
    "light cannot escape black holes",
    "comets are made of ice and dust",
    "asteroids are rocky objects",
    "the north star is polaris",
    "orion is a constellation",
    "andromeda is a galaxy",
    "the nearest star is the sun",
    "the speed of light is 186000 miles per second",
    
    # ===== TECHNOLOGY =====
    "computers understand binary language",
    "computers use binary code",
    "binary is 0 and 1",
    "the internet was created in the 1960s",
    "the world wide web was created in 1989",
    "tim berners lee invented the world wide web",
    "albert einstein developed the theory of relativity",
    "isaac newton discovered gravity",
    "galileo improved the telescope",
    "darwin published the theory of evolution",
    "watson and crick discovered dna structure",
    "marie curie discovered radium",
    "tesla invented the alternating current motor",
    "bell invented the telephone",
    "morse invented the telegraph",
    
    # ===== HUMAN FACTS =====
    "humans speak",
    "humans can speak",
    "people speak",
    "humans talk",
    "people talk",
    "humans use language",
    "humans communicate",
]


# ====== FAKE FACTS ======
KNOWN_FAKE_FACTS = [
    # ===== FLAT EARTH =====
    "earth is flat",
    "the earth is flat",
    "world is flat",
    "flat earth theory",
    "the world is flat",
    
    # ===== MOON CHEESE =====
    "moon is made of cheese",
    "the moon is made of cheese",
    
    # ===== SUN REVOLVES =====
    "sun revolves around the earth",
    "the sun revolves around the earth",
    "the sun goes around the earth",
    
    # ===== COMMON MYTHS =====
    "humans use only 10 percent of their brain",
    "humans only use 10% of their brain",
    "lightning never strikes the same place twice",
    "goldfish have a 3 second memory",
    "bats are blind",
    "ostriches bury their heads in sand",
    "cracking your knuckles causes arthritis",
    "eating carrots improves eyesight",
    "vaccines cause autism",
    "global warming is a hoax",
    "climate change is not real",
    "evolution is just a theory",
    "the earth is only 6000 years old",
    "dinosaurs lived with humans",
    "the moon landing was faked",
    "area 51 has aliens",
    "bigfoot is real",
    "the loch ness monster exists",
    "ghosts are real",
    "the bermuda triangle is mysterious",
    "crop circles are made by aliens",
    "5g causes covid",
    "covid is a hoax",
    "the government controls the weather",
    "election fraud is widespread",
    "the illuminati controls the world",
    "new world order is real",
    "the pyramids were built by aliens",
    "atlantis was a real place",
    "the fountain of youth exists",
    "the holy grail is real",
    "the titanic was unsinkable",
    "mars is populated by aliens",
    "ufos are alien spacecraft",
    "the earth is hollow",
    "hitler escaped to south america",
    "elvis is still alive",
    "tupac is still alive",
    "the apocalypse is coming",
    "2012 was the end of the world",
    "vampires are real",
    "werewolves are real",
    "zombies are real",
    "unicorns are real",
    "dragons are real",
    "mermaids are real",
    "psychic powers are real",
    "telepathy is real",
    "reincarnation is real",
    "fish speak english",
    "humans can breathe in space",
    "dinosaurs are still alive",
    "you can see the great wall from space",
    "sharks are immune to cancer",
    "we swallow 8 spiders a year",
    "camels store water in their humps",
    "bulls get angry at red color",
    "microwaves give you cancer",
    "cell phones cause brain cancer",
    "trump is prime minister of india",
    "donald trump is india's prime minister",
]

# Application settings
APP_CONFIG = {
    "debug": True,
    "host": "0.0.0.0",
    "port": 5000,
    "secret_key": "your-secret-key-change-in-production",
}