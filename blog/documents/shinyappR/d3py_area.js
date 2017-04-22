function draw(data) {
	var margin = {"left": 60, "height": 250, "right": 20, "width": 500, "bottom": 25, "top": 10};
	    width = 500 - margin.left - margin.right
	    height = 250 - margin.top - margin.bottom;
	var g = d3.select('#chart').append('svg').attr('width',width + margin.left + margin.right + 25).attr('height',height + margin.top + margin.bottom + 25).append('g').attr('transform','translate(' + margin.left + ',' + margin.top + ')')
	
        function get_scales(colnames, orientation){
            var this_data = d3.merge(
                colnames.map(
                    function(name){
                        return data.map(
                            function(d){
                                return d[name]
                            }
                        )
                    }
                )
            )
            if (orientation==="vertical"){
                if (isNaN(this_data[0])){
                    // not a number
                    console.log('using ordinal scale for vertical axis')
                    scale = d3.scale.ordinal()
                        .domain(this_data)
                        .range(d3.range(height,0,height/this_data.length))
                } else {
                    // a number
                    console.log('using linear scale for vertical axis')
                    extent = d3.extent(this_data)
                    extent[0] = extent[0] > 0 ? 0 : extent[0]
                    scale = d3.scale.linear()
                        .domain(extent)
                        .range([height,0])

                }
            } else {
                if (isNaN(this_data[0])){
                    // not a number
                    console.log('using ordinal scale for horizontal axis')
                    scale = d3.scale.ordinal()
                        .domain(this_data)
                        .rangeBands([0,width], 0.1)
                } else {
                    // a number
                    console.log('using linear scale for horizontal axis')
                    scale = d3.scale.linear()
                        .domain(d3.extent(this_data))
                        .range([0,width])
                }
            }
            return scale
        }
        
	
            scales = {
                x: get_scales(['x'], 'horizontal'),
                y: get_scales(['y0','y'], 'vertical')
            }
        
	var area = d3.svg.area().x(function(d) {
	return scales.x(d.x)
}
).y0(function(d) {
	return scales.y(d.y0)
}
).y1(function(d) {
	return scales.y(d.y)
}
)
	console.log(data)
	console.log(area(data))
	console.log(scales.y(data[0].y))
	g.append('svg:path').attr('d',area(data)).attr('class','geom_area').attr('id','area_x_y_y0')
	xAxis = d3.svg.axis().scale(scales.x)
	g.append("g").attr("class","xaxis").attr("transform","translate(0," + height + ")").call(xAxis)
	g.append("text").text("x").attr("text-anchor","middle").attr("x",width/2).attr("y",height+45)
	yAxis = d3.svg.axis().scale(scales.y).orient('left')
	g.append("g").attr("class","yaxis").call(yAxis)
	g.append("text").text("y").attr("y",- margin.left + 15).attr("x",- height / 2.0).attr("text-anchor","middle").attr("transform","rotate(-90, 0, 0)")
}

function init() {
}

