
function create_load_curve(element, csv, callback_simplified=false) {
   var x = [];
   var y = [];

   var call_axis = function (val, index) {
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

   if (callback_simplified) {
      call_axis = function (val, index) {
         if (index == 0) 
            return this.getLabelForValue("Janvier");
         else if (index == 31) 
            return this.getLabelForValue("Février");
         else if (index == 59) 
            return this.getLabelForValue("Mars");
         else if (index == 90) 
            return this.getLabelForValue("Avril");
         else if (index == 120) 
            return this.getLabelForValue("Mai");
         else if (index == 151) 
            return this.getLabelForValue("Juin");
         else if (index == 182) 
            return this.getLabelForValue("Juillet");
         else if (index == 212) 
            return this.getLabelForValue("Août");
         else if (index == 243) 
            return this.getLabelForValue("Septembre");
         else 
            return this.getLabelForValue("");
      }
   }

   csv.then( (data) => {
      let keys = Object.keys(data[0]);

      data.forEach(row => {
         x.push(row[keys[0]]);
         y.push(parseInt(row[keys[1]]));
      });

      element.classList.remove("loadingChart");
      new Chart(element, {
         type: 'line',
         data: {
         labels: x,
         datasets: [{
            label: 'Puissance sur un an',
            data: y,
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
                        callback : call_axis
                     }
                  },
                  y: {
                     beginAtZero: true
                  }
            }
         }
      });

   });
}

function create_load_mono_curve(element, csv){
   let d = [];
   let y = [...Array(101).keys()].reverse();
   csv.then( (data) => {
      let keys = Object.keys(data[0]);

      data.forEach(row => {
         d.push({
            "x": parseInt(row[keys[1]]),
            "y": parseInt(row[keys[0]])
         });
      });
      
      element.classList.remove("loadingChart");
      new Chart(element, {
         type: 'line',
         data: {
            labels:y,
            datasets: [{
                  label: 'Monotonne de puissance',
                  data: d,
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

   });
}
