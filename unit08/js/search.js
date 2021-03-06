// this function executes our search via an AJAX call
function runSearch() {
    // hide and clear the previous results, if any
    clearResults();

    // transforms all the form parameters into a string we can send to the server
    var frmStr = $("#gene_search").serialize();

    // run a search with the input data
    $.ajax({
        url: "./search_product.cgi",
        dataType: "json",
        data: frmStr,
        success: function (data, _textStatus, _jqXHR) {
            processJSON(data);
        },
        error: function (_jqXHR, textStatus, errorThrown) {
            alert("Failed to perform gene search! textStatus: (" + textStatus +
                ") and errorThrown: (" + errorThrown + ")");
        }
    });
}


// this processes a passed JSON structure representing gene matches and draws it 
// to the result table
function processJSON(data) {
    // set the span that lists the match count
    $("#match_count").text(data.match_count);

    // this will be used to keep track of row identifiers
    var next_row_num = 1;

    // iterate over each match and add a row to the result table for each
    $.each(data.matches, function (i, item) {
        var this_row_id = "result_row_" + next_row_num++;

        // create a row and append it to the body of the table
        $("<tr/>", { "id": this_row_id }).appendTo("tbody");

        // add the locus column
        $("<td/>", { "text": item.locus_id }).appendTo("#" + this_row_id);

        // add the product column
        $("<td/>", { "text": item.product }).appendTo("#" + this_row_id);

    });

    // now show the result section that was previously hidden
    $("#results").show();
}

// hide results and clear table
function clearResults() {
    $("#results").hide();
    $("tbody").empty();
}

// run our javascript once the page is ready
$(document).ready(function () {

    // autoccomplete function
    // run the autocomplete function
    $("#term").autocomplete({
        source: "./autocomplete.cgi",
        minLength: 0
    });

    // when reset button is clicked
    $("#reset").click(function () {
        // clear out search text
        $("#term").val("");
        // focus on text box
        $("#term").focus();
        // hide result table
        clearResults();
        return false; // prevents "normal" form submission
    });

    // define what should happen when a user clicks submit on our search form
    $("#submit").click(function () {
        // search for submitted text
        runSearch();
        // remove focus from search bar
        $("#term").blur();
        return false;  // prevents "normal" form submission
    });
});
