import os
from graphviz import Digraph

# Configure Graphviz path
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

# Create directed graph with paper-friendly settings
dot = Digraph(comment='AGV Workflow',
              format='pdf',  # Default format for initial rendering
              engine='dot',
              graph_attr={
                  'rankdir': 'TB',        # Top-Bottom layout
                  'size': '8.3,11.7',     # A4 paper dimensions (inches)
                  'ratio': 'compress',    # Optimize space
                  'nodesep': '0.4',       # Horizontal node separation
                  'ranksep': '0.6',       # Vertical separation between ranks
                  'fontname': 'Times New Roman',
                  'fontsize': '10',
                  'labelloc': 't',
                  'splines': 'ortho'      # Straight line connections
              },
              node_attr={
                  'shape': 'rect',
                  'style': 'rounded',
                  'fixedsize': 'true',
                  'width': '2.0',         # Uniform node width
                  'height': '0.8',        # Uniform node height
                  'fontname': 'Times New Roman',
                  'fontsize': '10'
              },
              edge_attr={
                  'arrowsize': '0.7',
                  'fontname': 'Times New Roman',
                  'fontsize': '9'
              })

# Define nodes
nodes = {
    'A': 'Standby in\nArea A (Charging)',
    'B1': 'Receive Sorting Order\nNavigate to Area B',
    'B2': 'Items in Area B?',
    'B3': 'Detect Item Color',
    'C': 'Scrap Processing\n(Area C)',
    'D': 'Reprocessing\n(Area D)',
    'E': 'Packaging\n(Area E)',
    'F': 'Repair\n(Area F)',
    'G': 'Quality Check\n(Area G)',
    'G_pass': 'QC Passed',
    'G_fail': 'QC Failed',
    'ReturnB': 'Return to Area B',
    'CheckBattery': 'Battery < 20%?',
    'ReturnA': 'Return to Area A'
}

for key, label in nodes.items():
    dot.node(key, label)

# Define edges with concise labels
edges = [
    ('A', 'B1', 'Sorting Order'),
    ('B1', 'B2', 'Arrived'),
    ('B2', 'A', 'No'),
    ('B2', 'B3', 'Yes'),
    ('B3', 'C', 'Red'),
    ('B3', 'E', 'Green'),
    ('B3', 'F', 'Blue'),
    ('C', 'D', 'Complete'),
    ('D', 'ReturnB', 'Done'),
    ('E', 'ReturnB', 'Done'),
    ('F', 'G', 'Repaired'),
    ('G', 'G_pass', 'Pass'),
    ('G', 'G_fail', 'Fail'),
    ('G_pass', 'E', 'Route'),
    ('G_fail', 'C', 'Route'),
    ('ReturnB', 'B2', ''),
    ('CheckBattery', 'ReturnA', 'Yes'),
    ('CheckBattery', 'ReturnB', 'No')
]

# Add battery check connections
for src in ['C', 'D', 'E', 'F', 'G']:
    dot.edge(src, 'CheckBattery', 'Battery Check')

for src, dst, label in edges:
    dot.edge(src, dst, label)

# Add invisible edges for layout alignment
with dot.subgraph() as s:
    s.attr(rank='same')
    s.edge('G_pass', 'G_fail', style='invis')

# Generate PDF (vector format for papers)
dot.render('agv_flow_paper', view=False, cleanup=True)

# Generate high-resolution PNG
dot.format = 'png'  # Switch to PNG format
dot.graph_attr['dpi'] = '300'  # Set DPI for high resolution
dot.render('agv_flow_high_res', view=False, cleanup=True)

print("PDF and PNG files generated successfully!")