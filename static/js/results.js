// Results comparison chart

const ctx =
    document.getElementById("resultsChart");


if (ctx) {

    new Chart(ctx, {

        type: "bar",

        data: {

            labels: [

                "Single Sensor",

                "Basic Fusion",

                "Trust-Aware Fusion"

            ],

            datasets: [

                {

                    label:
                        "Detection Confidence (%)",

                    data: [

                        78,
                        87,
                        93

                    ],

                    borderWidth: 1

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            scales: {

                y: {

                    beginAtZero: true,

                    max: 100,

                    title: {

                        display: true,

                        text:
                            "Detection Confidence (%)"

                    }

                }

            }

        }

    });

}