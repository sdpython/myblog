function draw(data) {
	var margin = {"left": 60, "height": 500, "right": 20, "width": 500, "bottom": 25, "top": 10};
	    width = 500 - margin.left - margin.right
	    height = 500 - margin.top - margin.bottom;
	var g = d3.select('#chart').append('svg').attr('width',width + margin.left + margin.right + 25).attr('height',height + margin.top + margin.bottom + 25).append('g').attr('transform','translate(' + margin.left + ',' + margin.top + ')')
	g.selectAll('circle.node').data(data.nodes).enter().append('circle').attr('class','node').attr('r',12)
	g.selectAll('line.link').data(data.links).enter().append('line').attr('class','link')
	var force = d3.layout.force()
	.charge(-120)
	.linkDistance(30)
	.size([width, height])
	.nodes(data.nodes)
	.links(data.links);force.on("tick", function() {
	g.selectAll("line.link").attr("x1", function(d) { return d.source.x; })
	.attr("y1", function(d) { return d.source.y; })
	.attr("x2", function(d) { return d.target.x; })
	.attr("y2", function(d) { return d.target.y; });
	g.selectAll("circle.node").attr("cx", function(d) { return d.x; })
	.attr("cy", function(d) { return d.y; });
	});
	g.selectAll("circle.node").call(force.drag);
	force.start();
}

function init() {
	console.debug('Hi');
}

