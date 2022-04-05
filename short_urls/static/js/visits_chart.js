document.addEventListener("DOMContentLoaded", function (event) {
  const analyticsText = document.getElementById("analytics").textContent;
  const analyticsData = JSON.parse(analyticsText);

  var data = [
    {
      x: analyticsData.map((datum) => datum["date"]),
      y: analyticsData.map((datum) => datum["visits_count"]),
      type: "scatter",
      mode: 'markers',
    },
  ];

  // Number of milliseconds in a day
  var oneDay = 86400000;
  var layout = {
    title: "Short URL visits",
    xaxis: {
      title: "Day",
      showgrid: false,
      zeroline: true,
      dtick: oneDay,
    },
    yaxis: {
      title: "Visit count",
      showline: false,
      rangemode: "tozero",
      dtick: 1,
    },
  };

  var config = {
      displayModeBar: false,
  };

  Plotly.newPlot("chart", data, layout, config);
});
