
var ctx = document.getElementById('myChart').getContext('2d');

var myChart = new Chart(ctx, {
	type: 'line',
	data: {
		labels: {{time}},
		datasets: [
			{label: 'NO2', data : {{aqualities}}, backgroundColor:['rgba(54, 162, 235, 0.2)'], borderColor: ['rgba(54, 162, 235, 1)'], borderWidth: 1}
		]
	},
	options: {
		scales: { yAxes: [{ ticks: { beginAtZero: false }}]}
	}
});

setInterval(function(){
	$.ajax({
		url:'/home/update_chart',
		success: function(test){
		    myChart.data.datasets[0].data = test.aqualities;
		    myChart.data.labels = test.time;
		    myChart.update();
		}
	    });
	}, 5000);
