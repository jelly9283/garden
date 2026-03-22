#!/usr/bin/env python3
"""
Extract wiki-style links from garden markdown files and build a graph JSON.
Wiki links format: [[filename]] or [[filename|display text]]
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

GARDEN_DIR = Path(__file__).parent / "garden"
OUTPUT_FILE = Path(__file__).parent / "graph-data.json"

def get_markdown_files():
    """Return list of all markdown files in garden/"""
    return sorted([f for f in GARDEN_DIR.glob("*.md")])

def normalize_filename(name):
    """
    Normalize a wiki link to actual filename.
    [[AI safety]] -> AI safety.md
    [[Some File|display text]] -> Some File.md
    """
    # Remove pipe and display text if present
    base_name = name.split("|")[0].strip()
    # Add .md extension if not present
    if not base_name.endswith(".md"):
        base_name += ".md"
    return base_name

def extract_links(file_path):
    """
    Extract all wiki-style links from a markdown file.
    Returns list of target filenames.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
    # Match [[...]] pattern, optionally with pipe for display text
    pattern = r'\[\[([^\]]+)\]\]'
    matches = re.findall(pattern, content)
    
    links = []
    for match in matches:
        normalized = normalize_filename(match)
        links.append(normalized)
    
    return links

def build_graph():
    """Build graph structure from all markdown files."""
    files = get_markdown_files()
    
    # Create node list
    nodes = []
    for file_path in files:
        node_id = file_path.stem  # filename without .md
        nodes.append({
            "id": node_id,
            "label": node_id,
            "title": node_id  # tooltip on hover
        })
    
    # Create edge list by checking which files exist
    edges = []
    edges_set = set()  # Track (source, target) pairs to avoid duplicates
    file_names = {f.name for f in files}
    file_stems = {f.stem for f in files}
    
    for file_path in files:
        source_id = file_path.stem
        links = extract_links(file_path)
        
        for link_target in links:
            # Try to find matching file
            target_stem = Path(link_target).stem
            
            # Check if target file exists
            if target_stem in file_stems:
                edge_key = (source_id, target_stem)
                if edge_key not in edges_set:
                    edges.append({
                        "from": source_id,
                        "to": target_stem,
                        "arrows": "to"
                    })
                    edges_set.add(edge_key)
    
    return {
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "total_files": len(files),
            "total_nodes": len(nodes),
            "total_edges": len(edges)
        }
    }

def main():
    print("Building graph from garden/ markdown files...")
    graph = build_graph()
    
    # Save to JSON
    OUTPUT_FILE.write_text(json.dumps(graph, indent=2), encoding="utf-8")
    
    print(f"✓ Graph saved to {OUTPUT_FILE}")
    print(f"  - Nodes: {graph['metadata']['total_nodes']}")
    print(f"  - Edges: {graph['metadata']['total_edges']}")
    print(f"  - Files: {graph['metadata']['total_files']}")

if __name__ == "__main__":
    main()
