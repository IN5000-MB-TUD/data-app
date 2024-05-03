$(document).ready(function(){
	"use_strict";

	let host = location.protocol + '//' + location.host;
	console.log("Ready at " + host);

	// Link events.
    $("#get_repository_data").click(function() {
		let repository_full_name = $("#repositories").val();
		let repository_information = getData(host + "/data/repository/" + repository_full_name + "/");
        let repository_data = getData(host + "/data/repository/" + repository_full_name + "/metrics/");

        $("#repository_information").html(JSON.stringify(repository_information));

        for (const [key, value] of Object.entries(repository_data.data)) {
            let csvData = "Date," + key + "\n";
            for (let i=0; i < value.length; i++) {
                let valueDate = value[i][0].split("T")[0];
                let valueCount = value[i][1];
                csvData += valueDate + "," + valueCount + "\n";
            }

            new Dygraph(
                // Containing div
                document.getElementById(key),
                // CSV or path to a CSV file.
                csvData,
                // Settings
                {
                    legend: "always",
                    title: key,
                    ylabel: "Count",
                }
            );
        }
	});

	// Init page.
	let repositoriesNames = getData(host + "/data/repository/");
    for (let i=0; i < repositoriesNames.data.length; i++) {
        $("#repositories").append($("<option />").val(repositoriesNames.data[i]).text(repositoriesNames.data[i]));
    }
});

/**
 * Fetch Data from APIs.
 * @param {*} url The API endpoint.
 * @returns The fetched data.
 */
function getData(url) {
	let returnData = {};
	$.ajax({
		url: url,
		type : "GET",
		async: false,
		success: function(data, status, xhr) {
			returnData = data;
		},
		error: function(xhr, status, error) {
			alert(status + "\n" + error + "\n" + JSON.stringify(xhr));
		}
	});
	return returnData;
}
