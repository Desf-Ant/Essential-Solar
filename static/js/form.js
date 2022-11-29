var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab



// Functions for tabs

function showTab(n) {
    //This function will display the specified tab of the form ...
    var x = document.getElementsByClassName("tab");
    console.log(x);
    x[n].style.display = "inline-block";
    // ... and fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Calcul !";
    } else {
        document.getElementById("nextBtn").innerHTML = "Suivant >";
    }

    // ... and run a function that displays the correct step indicator:
    fixStepIndicator(n)
}

function nextPrev(n) {
    var x = document.getElementsByClassName("tab");

    if (n == 1 && !validateForm()) return false;

    // Hide the current tab:
    x[currentTab].style.display = "none";

    currentTab = currentTab + n;

    if (currentTab >= x.length) {
        document.getElementById("regForm").submit();
        return false;
    }

    showTab(currentTab);
}

function validateForm() {

    // This function deals with validation of the form fields
    var x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");

    //A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {
        if (y[i].value == "") {
            y[i].className += " invalid";
            valid = false;
        }
    }

    //If the valid status is true, mark the step as finished and valid:
    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
        for (i = 0; i < y.length; i++)
            y[i].className = "input";
    }
    return valid; // return the valid status
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    var y = document.getElementsByClassName("path-row");

    for (i = 0; i < x.length; i++) {
        x[i].className = "step";
    }
    for (i = 0; i < y.length; i++) {
        y[i].className = "path-row";
    }


    for (i = 0; i < n; i++)
        y[i].className = "path-row finish";

    if (n - 1 >= 0)
        y[n-1].className = "path-row active";

    for (i = 0; i < n; i++)
        x[i].className = "step finish";
    x[n].className += " active";
}
