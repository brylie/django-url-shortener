document.addEventListener("DOMContentLoaded", function (event) {
  const analyticsText = document.getElementById("analytics").textContent;
  const analyticsData = JSON.parse(analyticsText);

  var data = [
    {
      x: analyticsData.map((datum) => datum["date"]),
      y: analyticsData.map((datum) => datum["visits_count"]),
      type: "scatter",
    },
  ];

  var layout = {
    title: "Short URL visits",
    xaxis: {
      title: "Day",
      showgrid: false,
      zeroline: true,
    },
    yaxis: {
      title: "Visit count",
      showline: false,
      rangemode: "tozero",
    },
  };

  var config = {
      displayModeBar: false,
  };

  Plotly.newPlot("chart", data, layout, config);
});
