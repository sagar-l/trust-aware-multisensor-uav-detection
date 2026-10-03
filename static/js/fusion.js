// Trust-weighted fusion

const fusionData = {

    Radar: {
        evidence: 95,
        trust: 94
    },

    RF: {
        evidence: 92,
        trust: 89
    },

    "EO/IR": {
        evidence: 90,
        trust: 91
    }

};


// Calculate weighted confidence

let numerator = 0;
let denominator = 0;

for (const sensor in fusionData) {

    const evidence = fusionData[sensor].evidence;
    const trust = fusionData[sensor].trust;

    numerator += evidence * trust;

    denominator += trust;

}


const finalConfidence = numerator / denominator;

console.log(
    "Calculated Fusion Confidence:",
    finalConfidence.toFixed(2) + "%"
);


// Chart

const ctx = document.getElementById("fusionChart");

if (ctx) {

    new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: [
                "Radar",
                "RF",
                "EO/IR"
            ],

            datasets: [

                {
                    data: [
                        40,
                        28,
                        32
                    ],

                    borderWidth: 1
                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}