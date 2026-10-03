// Normal sensor trust values

const normalTrust = {

    Radar: 94,

    RF: 89,

    "EO/IR": 91

};


// Normal detection confidence

const normalConfidence = 93;


// Failure condition effects

const conditionEffects = {

    Normal: 1.00,

    Noisy: 0.75,

    Degraded: 0.50,

    Unavailable: 0.00

};


// Get HTML elements

const sensorSelect =
    document.getElementById("sensorSelect");

const conditionSelect =
    document.getElementById("conditionSelect");

const runButton =
    document.getElementById("runFailureTest");


// Run test

runButton.addEventListener("click", function () {

    const selectedSensor =
        sensorSelect.value;

    const condition =
        conditionSelect.value;


    const originalTrust =
        normalTrust[selectedSensor];


    const multiplier =
        conditionEffects[condition];


    const newTrust =
        Math.round(originalTrust * multiplier);


    // Calculate confidence reduction

    let confidenceAfter =
        normalConfidence;


    if (condition === "Noisy") {

        confidenceAfter = 89;

    }

    else if (condition === "Degraded") {

        confidenceAfter = 86;

    }

    else if (condition === "Unavailable") {

        confidenceAfter = 84;

    }


    // Update result boxes

    document.getElementById("trustBefore")
        .textContent = originalTrust + "%";


    document.getElementById("trustAfter")
        .textContent = newTrust + "%";


    document.getElementById("confidenceBefore")
        .textContent = normalConfidence + "%";


    document.getElementById("confidenceAfter")
        .textContent = confidenceAfter + "%";


    // Update message

    const resultMessage =
        document.getElementById("resultMessage");


    if (condition === "Normal") {

        resultMessage.className =
            "alert alert-success mt-3";

        resultMessage.textContent =
            selectedSensor +
            " operating normally.";

    }

    else if (condition === "Noisy") {

        resultMessage.className =
            "alert alert-warning mt-3";

        resultMessage.textContent =
            selectedSensor +
            " is experiencing noisy measurements. " +
            "Trust has been reduced.";

    }

    else if (condition === "Degraded") {

        resultMessage.className =
            "alert alert-warning mt-3";

        resultMessage.textContent =
            selectedSensor +
            " is degraded. " +
            "The fusion system is relying more heavily on the remaining sensors.";

    }

    else {

        resultMessage.className =
            "alert alert-danger mt-3";

        resultMessage.textContent =
            selectedSensor +
            " unavailable — decision calculated using remaining sensors.";

    }


    // Update sensor table

    updateSensorTable(
        selectedSensor,
        newTrust,
        condition
    );


    // Show result

    document.getElementById("resultSection")
        .style.display = "block";

});


// Update sensor table

function updateSensorTable(
    selectedSensor,
    newTrust,
    condition
) {

    const trustElementMap = {

        Radar: "radarTrust",

        RF: "rfTrust",

        "EO/IR": "eoirTrust"

    };


    const statusElementMap = {

        Radar: "radarStatus",

        RF: "rfStatus",

        "EO/IR": "eoirStatus"

    };


    // Reset all sensors

    document.getElementById("radarTrust")
        .textContent = "94%";

    document.getElementById("rfTrust")
        .textContent = "89%";

    document.getElementById("eoirTrust")
        .textContent = "91%";


    document.getElementById("radarStatus")
        .innerHTML =
        '<span class="badge bg-success">Active</span>';

    document.getElementById("rfStatus")
        .innerHTML =
        '<span class="badge bg-success">Active</span>';

    document.getElementById("eoirStatus")
        .innerHTML =
        '<span class="badge bg-success">Active</span>';


    // Update selected sensor

    document.getElementById(
        trustElementMap[selectedSensor]
    ).textContent =
        newTrust + "%";


    let statusText = "Active";

    let badgeClass = "bg-success";


    if (condition === "Noisy") {

        statusText = "Noisy";

        badgeClass = "bg-warning";

    }

    else if (condition === "Degraded") {

        statusText = "Degraded";

        badgeClass = "bg-warning";

    }

    else if (condition === "Unavailable") {

        statusText = "Unavailable";

        badgeClass = "bg-danger";

    }


    document.getElementById(
        statusElementMap[selectedSensor]
    ).innerHTML =
        `<span class="badge ${badgeClass}">
            ${statusText}
        </span>`;

}