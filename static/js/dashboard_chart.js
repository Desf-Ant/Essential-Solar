const ct1 = document.getElementById('conso_annuelle_chart');
const ct2 = document.getElementById('monotone_puissance_chart');

console.log("ok");

d3.csv("static/data/monotone_puissance_lycee_cassin.csv", function(data) {
   for (var i = 0; i < data.length; i++) {
       console.log(data[i]);
   }
});

// var data = JSON.parse('{{ conso_annuelle | safe }}');
var data = [1,2,1,4,5];
new Chart(ct1, {
   type: 'line',
   data: {
   labels: Array.from(Array(data.length).keys()),
   datasets: [{
      label: 'Puissance sur un an',
      data: data,
      borderWidth: 1
   }]
   },
   options: {
      elements: {
            point:{
               radius: 0
            }
      },
      scales: {
            x: {
               ticks : {
                  callback : function (val, index) {
                        if (index == 0) 
                           return this.getLabelForValue("Janvier");
                        else if (index == 4466) 
                           return this.getLabelForValue("Février");
                        else if (index == 8498) 
                           return this.getLabelForValue("Mars");
                        else if (index == 12956) 
                           return this.getLabelForValue("Avril");
                        else if (index == 17276) 
                           return this.getLabelForValue("Mai");
                        else if (index == 21740) 
                           return this.getLabelForValue("Juin");
                        else if (index == 26060) 
                           return this.getLabelForValue("Juillet");
                        else if (index == 30524) 
                           return this.getLabelForValue("Août");
                        else if (index == 34988) 
                           return this.getLabelForValue("Septembre");
                        else 
                           return this.getLabelForValue("");
                  }
               }
            },
            y: {
               beginAtZero: true
            }
      }
   }
});

// var freq_cumul = JSON.parse('{{ freq_cumul | safe }}');
// var conso_monotone = JSON.parse('{{ conso_monotone | safe }}');
var freq_cumul = [1,0.6,0.5];
var conso_monotone = [1,8,19];
new Chart(ct2, {
   type: 'line',
   data: {
      labels:freq_cumul,
      datasets: [{
            label: 'Monotonne de puissance',
            data: conso_monotone,
            borderWidth: 1
      }]
   },
   options: {
      elements: {
            point:{
               radius: 0
            }
      },
      x: {
            type: 'linear',
            ticks : {
               reverse: false,
               stepSize: 0.05
            }
      },
      y: {
            beginAtZero: true
      }
      }
});