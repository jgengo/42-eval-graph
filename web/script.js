const svg = d3.select("svg"),
	  width = window.innerWidth,
	  height = window.innerHeight;

// Add a container for zooming
const container = svg.append("g");

const tooltip = d3.select("body").append("div")
	.attr("class", "tooltip");

const color = d3.scaleOrdinal(d3.schemePastel2);

const simulation = d3.forceSimulation()
	.force("link", d3.forceLink().id(d => d.id))
	.force("charge", d3.forceManyBody().strength(-300))
	.force("center", d3.forceCenter(width / 2, height / 2));

d3.json("./data.json").then(function(data) {
	const link = container.append("g")
		.attr("class", "links")
		.selectAll("line")
		.data(data.links)
		.enter().append("line")
		.attr("class", (d) => `link ${d.value > 5 ? "alert" : "ok"}`)
		.attr("stroke-width", d => Math.sqrt(d.value))
		.on("mouseover", function(event, d) {
			tooltip.transition()
				.duration(200)
				.style("opacity", .9);
			tooltip.html(`${d.source.id} ↔ ${d.target.id}<br/>${d.value} evaluations`)
				.style("left", (event.pageX + 5) + "px")
				.style("top", (event.pageY - 28) + "px");
		})
		.on("mouseout", function() {
			tooltip.transition()
				.duration(500)
				.style("opacity", 0);
		});

	const node = container.append("g")
		.attr("class", "nodes")
		.selectAll("g")
		.data(data.nodes)
		.enter().append("g")
		.attr("class", "node")
		.on("mouseover", function(event, d) {
			tooltip.transition()
				.duration(200)
				.style("opacity", .9);
			tooltip.html(`${d.id}`)
				.style("left", (event.pageX + 5) + "px")
				.style("top", (event.pageY - 28) + "px");
			d3.select(this).select(".label").style("visibility", "visible");
		})
		.on("mouseout", function() {
			tooltip.transition()
				.duration(500)
				.style("opacity", 0);
			d3.select(this).select(".label").style("visibility", "hidden");
		});

	node.append("circle")
		.attr("r", 5)
		.attr("fill", d => color(d.group));

	node.append("text")
		.attr("class", "label")
		.attr("x", 8)
		.attr("y", 3)
		.text(d => d.id);

	node.call(d3.drag()
		.on("start", dragstarted)
		.on("drag", dragged)
		.on("end", dragended));

	simulation
		.nodes(data.nodes)
		.on("tick", ticked);

	simulation.force("link")
		.links(data.links);

	function ticked() {
		link
			.attr("x1", d => d.source.x)
			.attr("y1", d => d.source.y)
			.attr("x2", d => d.target.x)
			.attr("y2", d => d.target.y);

		node
			.attr("transform", d => `translate(${d.x},${d.y})`);
	}

	function dragstarted(event, d) {
		if (!event.active) simulation.alphaTarget(0.3).restart();
		d.fx = d.x;
		d.fy = d.y;
	}

	function dragged(event, d) {
		d.fx = event.x;
		d.fy = event.y;
	}

	function dragended(event, d) {
		if (!event.active) simulation.alphaTarget(0);
		d.fx = d.x;
		d.fy = d.y;
	}

	function filterNodes() {
	const isChecked = d3.select("#filterCheckbox").property("checked");

	if (isChecked) {
		// Hide nodes without any link with value > 5
		node.style("opacity", function(d) {
			const hasHighValueLink = data.links.some(link =>
				(link.source.id === d.id || link.target.id === d.id) && link.value > 5
			);
			return hasHighValueLink ? 1 : 0;
		});

		// Hide links with value <= 5
		link.style("opacity", d => d.value > 5 ? 1 : 0);
	} else {
		// Show all nodes and links
		node.style("opacity", 1);
		link.style("opacity", 1);
	}
}

	d3.select("#filterCheckbox").on("change", filterNodes);

	function searchNode() {
	const searchValue = d3.select("#searchBox").property("value").toLowerCase();
	const foundNode = data.nodes.find(node => node.id.toLowerCase() === searchValue);

	if (foundNode) {
		node.select("circle")
			.attr("r", 5) // Reset all node sizes
			.attr("fill", d => color(d.group)); // Reset all node colors

		// Highlight the found node
		const highlightedNode = d3.select(node.nodes().find(n => n.__data__.id === foundNode.id))
								.select("circle")
								.attr("r", 10) // Increase the size
								.attr("fill", "orange"); // Change color to orange

		// Zoom into the found node
		const scale = 2;
		const translate = [width / 2 - scale * foundNode.x, height / 2 - scale * foundNode.y];
		container.transition()
			.duration(750)
			.attr("transform", `translate(${translate})scale(${scale})`);
	} else {
		alert("Student not found");
	}
}

// Add event listener to the search box
d3.select("#searchBox").on("keyup", function(event) {
	if (event.key === "Enter") {
		searchNode();
	}
});

});

// Apply zoom and pan behavior
svg.call(d3.zoom()
	.extent([[0, 0], [width, height]])
	.scaleExtent([0.1, 8])
	.on("zoom", zoomed));

function zoomed(event) {
	container.attr("transform", event.transform);
}

// Resize SVG when window is resized
window.addEventListener('resize', function() {
	svg.attr('width', window.innerWidth)
	   .attr('height', window.innerHeight);
	simulation.force("center", d3.forceCenter(window.innerWidth / 2, window.innerHeight / 2));
	simulation.alpha(1).restart();
});
