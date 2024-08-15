<h1 align="center"><code>42-eval-graph</code></h1>

<div align="center">
  <sub>Created by <a href="">Jordane Gengo (Titus)</a></sub>
</div>

<h1 align="center">Proof-of-Concept</h1>

This project is a simple Proof-of-Concept for the 42network allowing to visualize the evaluations made via a network graph.

![example](.github/docs/image0.png)

<br>
<br>

![example link](.github/docs/image1.png)

## Requirements

- 42API app
- Python 3.6+ (tested with 3.12)

## How to run

Create a venv
```
python3 -m venv venv
```

Activate your venv
```
source venv/bin/activate
```

Add the information to your config.yml
```
cp config.sample.yml config.yml
```

```
python pull.py
```

The previous command will create a data.json file inside `./web` directory

<br><br>

The easiest way to run a little web server to open the website is to go inside web/ folder and run a http server with python
```
cd web/ && python3 -m http.server
```

Your network graph should then be accessible from http://localhost:8000/

<br>

## Potential ideas

- Cluster Detection and Visualization (js-louvain)
- Interactive Info Panel (instead of tooltip)
- Time-Based Filtering
- Heatmap Overlay
- Export Graph as Image
