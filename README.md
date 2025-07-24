# The-OFf-SETT Framework Toolkit
The OFf-SETT Framework Toolkit

## Overview

The **OFf‑SETT Framework Toolkit** is a suite of resources for exploring and querying **SeTT** — a multi-layered ontology designed to represent semantic trajectories of Territorial Units within the Linked Open Data (LOD) cloud. It includes:

- **Exploration scripts** for analyzing the SeTT Knowledge Graph (SeTT-KG), populated with:
  - **Spectral indices data** (e.g., NDVI, Surface Temperature, NDWI, NDSI, NDBI)
  - **Demographic data** (e.g., municipal population)
- **SPARQL queries** to explore semantic trajectories and semantic data cubes
- References to ontology definitions provided in the `TheSeTTOntology/` directory


---

## Repository Structure

    ├── ExplorationScripts/     # Dataset and Notebooks for interactive analysis
    ├── SPARQLQueries/         # Pre‑defined SPARQL query files for exploration
    ├── TheSeTTOntology/       # Underlying ontology files (.ttl, .owl)
    ├── .gitignore
    └── README.md

---

##  Getting Started

### Requirements

- Python ≥ 3.x  
- Jupyter Notebook or JupyterLab  
- RDF/SPARQL libraries:

### How It Works

- **SeTT Ontology** models raw, structured, and semantic trajectories that describe the evolution of Territorial Units across various themes such as vegetation, temperature, and population.

ExplorationScripts provide Jupyter notebooks for querying and visualizing the SeTT-KG. The data focuses on the study areas of Evian, Fribourg, and Grand Genève, located in France and Switzerland.
- **ExplorationScripts** include Python notebooks for querying and visualizing the SeTT-KG populated with study area data, namely Evian, Fribourg, and Grand Geneve; located at France and Switzerland.
- **SPARQLQueries** folder includes a set of pre-written SPARQL queries to extract structured knowledge and recurring patterns from the knowledge graph.

##  More information on SeTT ontology and SeTT-KG

### SeTT ontology documentation webpage
    [http://steamerlod.imag.fr/
    Select the TRACES_KG_TRAJECTORIES repository](https://danielafe7-personal.github.io/TheSeTTOntology/)

### SPARQL endpoint URL
 http://steamerlod.imag.fr/
 Select the TRACES_KG_TRAJECTORIES repository


## Contact

Questions or feedback? Open an issue on GitHub or reach out to **daniela.milon-flores@univ-grenoble-alpes.fr ; dmilonflores@gmail.com ; camille.bernard@univ-grenoble-alpes.fr ; jerome.gensel@univ-grenoble-alpes.fr ; gregory.giuliani@unige.ch**.

