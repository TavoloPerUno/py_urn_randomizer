# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath("../"))

# -- Project information -----------------------------------------------------

project = "Urn Randomizer"
copyright = "2021-2026, Research Computing Group, University of Chicago"
author = "Research Computing Group, University of Chicago"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinxcontrib.autohttp.flask",
    "sphinx.ext.autodoc",
    "sphinx_click.ext",
    "sphinx_design",
    "sphinx_sitemap",
    "sphinxext.opengraph",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#800000",
        "color-brand-content": "#800000",
        "color-admonition-title--tip": "#7EBEC5",
        "color-admonition-title-background--tip": "#7EBEC510",
    },
    "dark_css_variables": {
        "color-brand-primary": "#c06060",
        "color-brand-content": "#c06060",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/TavoloPerUno/py_urn_randomizer",
            "html": '<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>',
            "class": "",
        },
    ],
}

html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_logo = "figures/logo-docs.png"
html_favicon = "figures/favicon.ico"
html_title = "Urn Randomizer"

autodoc_member_order = "groupwise"
numfig = True

# Suppress warnings about missing references in autoflask
suppress_warnings = ["ref.any"]

# --- Sitemap ---
html_baseurl = "https://tavoloperuno.github.io/py_urn_randomizer/"
sitemap_url_scheme = "{link}"

# --- robots.txt ---
html_extra_path = ["_static/robots.txt", "_static/googlef63886eaa754b15d.html"]

# --- SEO meta tags ---
html_meta = {
    "description": (
        "Urn Randomizer — a clinical trial urn randomization system "
        "implementing the adaptive biased coin design by Wei (1978), "
        "with a Flask web GUI, REST API, and CLI."
    ),
    "keywords": (
        "urn randomization, clinical trials, adaptive biased coin, "
        "treatment allocation, stratified randomization, Flask, "
        "Wei 1978, biostatistics, RCT"
    ),
}

# --- Open Graph (social sharing) ---
ogp_site_url = "https://tavoloperuno.github.io/py_urn_randomizer/"
ogp_site_name = "Urn Randomizer"
ogp_description_length = 200
ogp_type = "website"
