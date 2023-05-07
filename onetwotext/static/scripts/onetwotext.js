window.onload = function(argument) {

	var lyric = "Tyger! Tyger! Burning bright In the forests of the night: What immortal hand or eye Could frame thy fearful symmetry? In what distant deeps or skies Burnt the fire of thine eyes? On what wings dare he aspire? What the hand dare seize the fire? And what shoulder, and what art, Could twist the sinews of thy heart? And when thy heart began to beat, What dread hand? And what dread feet? What the hammer? What the chain? In what furnace was thy brain? What the anvil? What dread grasp Dare its deadly terrors clasp? When the stars threw down their spears, And water'd heaven with their tears: Did He smile His work to see?Did He who made the Lamb make thee? Tyger! Tyger! Burning bright In the forests of the night: What immortal hand or eye Dare frame thy fearful symmetry? Tyger! Tyger! Burning bright In the forests of the night: What immortal hand or eye Could frame thy fearful symmetry? In what distant deeps or skies Burnt the fire of thine eyes? On what wings dare he aspire? What the hand dare seize the fire? And what shoulder, and what art, Could twist the sinews of thy heart? And when thy heart began to beat, What dread hand? And what dread feet? What the hammer? What the chain? In what furnace was thy brain? What the anvil? What dread grasp Dare its deadly terrors clasp? When the stars threw down their spears, And water'd heaven with their tears: Did He smile His work to see?Did He who made the Lamb make thee? Tyger! Tyger! Burning bright In the forests of the night: What immortal hand or eye Dare frame thy fearful symmetry? Tyger! Tyger! Burning bright In the forests of the night: What immortal hand or eye Could frame thy fearful symmetry? In what distant deeps or skies Burnt the fire of thine eyes? On what wings dare he aspire? What the hand dare seize the fire? And what shoulder, and what art, Could twist the sinews of thy heart? And when thy heart began to beat, What dread hand? And what dread feet? What the hammer? What the chain? In what furnace was thy brain? What the anvil? What dread grasp Dare its deadly terrors clasp? When the stars threw down their spears, And water'd heaven with their tears: Did He smile His work to see?Did He who made the Lamb make thee? Tyger! Tyger! Burning bright In the forests of the night: What immortal hand or eye Dare frame thy fearful symmetry?";
	var words = {};
	var words_attr = [];
	string_handle(lyric);

	var canvas = document.getElementById('c');
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;

	if (canvas.getContext) {
		var c = canvas.getContext('2d'),
			w = canvas.width,
			h = canvas.height;

		c.strokeStyle = 'red';
		c.fillStyle = 'white';
		c.lineWidth = 5;

		// constructor
		Word = function(key) {
			this.text = key;
			this.x = Math.random() * w;
			this.y = Math.random() * h;
			this.font = words[key] * 10 + 'px arial'
			this.speed = (words[key]);
		}
		for (key in words) {
			words_attr.push(new Word(key));
		}
		console.log(words_attr.length);

		function animation() {
			for (var i = 0; i < words_attr.length; i++) {
				c.font = words_attr[i].font;
				c.fillText(words_attr[i].text, words_attr[i].x, words_attr[i].y);
				words_attr[i].width = c.measureText(words_attr[i].text).width;
				c.stroke();
			}
			move();
		}

		function move() {
			for (var i = 0; i < words_attr.length; i++) {
				if (words_attr[i].x > w) {
					words_attr[i].x = -words_attr[i].width;
					words_attr[i].y = Math.random()*h;
				}else{
					words_attr[i].x += words_attr[i].speed;
				}
			}
		}

		setInterval(function() {
			c.clearRect(0,0,w,h);
			animation();
		},24);

	}

	function string_handle(str) {
		var split_str = str.split(" ");
		var word_array = [];
		var word_count = [];
		for (var i = 0; i < split_str.length; i++) {
			check = true;
			for (var j = 0; j <= word_array.length; j++) {
				if (split_str[i] == word_array[j]) {
					word_count[j]++;
					check = false;
					break;
				}
			}
			if (check) {
				word_array.push(split_str[i]);
				word_count.push(1);
			}
		}
		for (var i = 0; i < word_array.length; i++) {
			words[word_array[i]] = word_count[i];
		}
		return words;
	}
}


// Gestisci il click sul pulsante "Submit"
document.getElementById("submit-button").addEventListener("click", function () {
    event.preventDefault();
    const textarea = document.getElementById('text-input');
    const text = textarea.value.trim();
    
    // Controlla se la textarea è vuota
    if (textarea.value.trim() === '') {
        // Mostra un popup con un messaggio di avviso
        alert('You must write text to count!');
        return;
    }
    // Esegui una chiamata AJAX POST per ottenere la risposta
    fetch("/count-text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    })
      .then(function(response) {
          return response.json();
      })
      .then(function(response) {
        scrollToFooter();

        const responseContainer = document.getElementById("response-container");
        const numWords = response.num_words;
        let count = 0;
        responseContainer.innerText = count;
        responseContainer.style.fontSize = "0cm";
        setTimeout(() => {
          responseContainer.style.fontSize = "4cm";
          const interval = setInterval(() => {
            count++;
            responseContainer.innerText = count;
            if (count === numWords) {
              clearInterval(interval);
            }
          }, 50);
        }, 100);
  
        // Crea l'array di valori per l'istogramma
        const freqList = response.word_freq;
        const values = freqList.map((item) => Object.values(item)[0]);

        // Crea l'array di etichette per l'istogramma
        const labels = freqList.map((item) => Object.keys(item)[0]);

        // Calcola la scala massima per la y, arrotondata all'intero superiore
        const maxY = Math.ceil(Math.max(...values)/10)*10;

        // Crea l'oggetto di layout per l'istogramma
        const layout = {
            title: {
              text: 'Words Frequency',
              font: {
                size: 28,
                color: 'white'
              }
            },
            xaxis: {
              tickangle: -45,
              tickfont: {
                color: 'white'
              },
              title: {
                text: 'Words',
                font: {
                  size: 20,
                  color: 'white'
                }
              }
            },
            yaxis: {
                title: {
                  text: 'Count',
                  font: {
                    size: 20,
                    color: 'white'
                  }
                },
                tickfont: {
                  color: 'white'
                },
                tickmode: 'linear',
                tick0: 0,
                dtick: 1
              },
            bargap: 0.05,
            plot_bgcolor: 'black',
            paper_bgcolor: 'black',
            font: {
              color: 'white'
            },
            barmode: 'group',
            bargroupgap: 0.2,
            marker: {
              color: ['#FF4136', '#0074D9', '#2ECC40', '#FF851B', '#7FDBFF', '#F012BE', '#B10DC9', '#01FF70']
            }
          };

        // Crea l'oggetto di traccia per l'istogramma
        const trace = {
            x: labels,
            y: values,
            type: 'bar'
        };

        // Crea l'array di tracce per il grafico
        const data = [trace];

        // Crea il grafico utilizzando Plotly
        Plotly.newPlot('histogram-container', data, layout);

        // Crea l'array di valori per il grafico a torta
        const pieValues = freqList.map((item) => Object.values(item)[0]);

        // Crea l'array di etichette per il grafico a torta
        const pieLabels = freqList.map((item) => Object.keys(item)[0]);

        // Crea l'oggetto di layout per il grafico a torta
        const pieLayout = {
        title: {
            text:'Frequency Words - Pie Chart',
            font:{
                size: 28,
                color: 'white',
            }
        },
        paper_bgcolor: '#000',
        plot_bgcolor: '#000',
        };

        // Crea l'oggetto di traccia per il grafico a torta
        const pieTrace = {
        values: pieValues,
        labels: pieLabels,
        type: 'pie'
        };

        // Crea l'array di tracce per il grafico a torta
        const pieData = [pieTrace];

        // Crea il grafico a torta utilizzando Plotly
        Plotly.newPlot('pie-chart-container', pieData, pieLayout);
      })
  });


document.getElementById("ai-button").addEventListener("click", function () {
    event.preventDefault();
    const textarea = document.getElementById('text-input');
    const text = textarea.value.trim();

    if (textarea.value.trim() === '') {
        // Mostra un popup con un messaggio di avviso
        alert('You must write text to count!');
        return;
    }

    // Controlla la lunghezza del testo
    const words = text.split(" ");
    if (words.length > 80) {
        // Mostra un popup di avviso
        const proceed = confirm('The maximum number of words allowed is 80. Proceed anyway?');
        if (!proceed) {
            return;
        }
    }

    document.getElementById("ai-button").classList.add("loading");
    document.getElementById("ai-button").innerText = "Running";
    // Execute AJAX POST to obtain response
    fetch("/count-from-ai", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    })
      .then(function(response) {
          return response.json();
      })
      .then(function(response) {
        document.getElementById("ai-button").classList.remove("loading");
        document.getElementById("ai-button").innerText = "Ask the AI";
        scrollToFooter();     
        const responseContainer = document.getElementById("response-container");
        const numWords = response.num_words;
        let count = 0;
        responseContainer.innerText = count;
        responseContainer.style.fontSize = "0cm";
        setTimeout(() => {
          responseContainer.style.fontSize = "4cm";
          const interval = setInterval(() => {
            count++;
            responseContainer.innerText = count;
            if (count === numWords) {
              clearInterval(interval);
            }
          }, 50);
        }, 100);
  
        // Crea l'array di valori per l'istogramma
        const freqList = response.word_freq;
        const values = freqList.map((item) => Object.values(item)[0]);

        // Crea l'array di etichette per l'istogramma
        const labels = freqList.map((item) => Object.keys(item)[0]);

        // Calcola la scala massima per la y, arrotondata all'intero superiore
        const maxY = Math.ceil(Math.max(...values)/10)*10;

        // Crea l'oggetto di layout per l'istogramma
        const layout = {
            title: {
              text: 'Words Frequency',
              font: {
                size: 28,
                color: 'white'
              }
            },
            xaxis: {
              tickangle: -45,
              tickfont: {
                color: 'white'
              },
              title: {
                text: 'Words',
                font: {
                  size: 20,
                  color: 'white'
                }
              }
            },
            yaxis: {
                title: {
                  text: 'Count',
                  font: {
                    size: 20,
                    color: 'white'
                  }
                },
                tickfont: {
                  color: 'white'
                },
                tickmode: 'linear',
                tick0: 0,
                dtick: 1
              },
            bargap: 0.05,
            plot_bgcolor: 'black',
            paper_bgcolor: 'black',
            font: {
              color: 'white'
            },
            barmode: 'group',
            bargroupgap: 0.2,
            marker: {
              color: ['#FF4136', '#0074D9', '#2ECC40', '#FF851B', '#7FDBFF', '#F012BE', '#B10DC9', '#01FF70']
            }
          };

        // Crea l'oggetto di traccia per l'istogramma
        const trace = {
            x: labels,
            y: values,
            type: 'bar'
        };

        // Crea l'array di tracce per il grafico
        const data = [trace];

        // Crea il grafico utilizzando Plotly
        Plotly.newPlot('histogram-container', data, layout);

        // Crea l'array di valori per il grafico a torta
        const pieValues = freqList.map((item) => Object.values(item)[0]);

        // Crea l'array di etichette per il grafico a torta
        const pieLabels = freqList.map((item) => Object.keys(item)[0]);

        // Crea l'oggetto di layout per il grafico a torta
        const pieLayout = {
        title: {
            text: 'Titolo del grafico a torta',
            font: {
                size: 28,
                color: 'white'
            }
        },
        paper_bgcolor: '#000',
        plot_bgcolor: '#000',
        };

        // Crea l'oggetto di traccia per il grafico a torta
        const pieTrace = {
        values: pieValues,
        labels: pieLabels,
        type: 'pie'
        };

        // Crea l'array di tracce per il grafico a torta
        const pieData = [pieTrace];

        // Crea il grafico a torta utilizzando Plotly
        Plotly.newPlot('pie-chart-container', pieData, pieLayout);
      })
  });

// Gradual scroll to footer
const footer = document.getElementById('footer');
const scrollToFooter = () => {
  const distanceToTop = footer.getBoundingClientRect().top;
  const duration = 1500; // milliseconds
  const start = window.pageYOffset;
  let startTime = null;

  const ease = (t, b, c, d) => {
    t /= d / 2;
    if (t < 1) return c / 2 * t * t + b;
    t--;
    return -c / 2 * (t * (t - 2) - 1) + b;
  };

  const animation = (currentTime) => {
    if (startTime === null) startTime = currentTime;
    const timeElapsed = currentTime - startTime;
    const run = ease(timeElapsed, start, distanceToTop, duration);
    window.scrollTo(0, run);
    if (timeElapsed < duration) requestAnimationFrame(animation);
  };
  requestAnimationFrame(animation);
};

