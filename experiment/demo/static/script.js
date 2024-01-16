$(function () {
    var typing = false;

    function init() {
        $("#news").hide();
        $("#reset_button").hide();
        $("#generate_button").show();
        $("#generate_button").prop('disabled', false);
        $("#start-icon").show();
        $("#loading-icon").hide();
        $("#news_content").html("");
        typing = false;
    }
    init();

    $("#generate_button").click(function () {
        $("#generate_button").prop('disabled', true);
        $("#start-icon").hide();
        $("#loading-icon").show();

        let file = $('#input_file')[0].files[0];
        let model = $('#input_model').val();
        console.log("file:", file)
        console.log("model:", model)

        if (file != undefined){
            if (file["type"] == "text/csv") {
                let fd = new FormData();
                fd.append('file', file);
                fd.append('model', model);
                // console.log("fd:", fd)

                $.ajax({
                    url: '/pipeline',
                    type: 'post',
                    data: fd,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        console.log("response:", response)
                        let state = response["state"]
                        let content = response["content"]

                        if (state == "success") {
                            // alert('Generate success!');
                            $("#news").show();
                            $("#reset_button").show();
                            $("#generate_button").hide();

                            let i = 0;
                            let speed = 25; /* The speed/duration of the effect in milliseconds */
                            typing = true

                            function typeWriter() {
                                if (i < content.length && typing) {
                                    document.getElementById("news_content").innerHTML += content.charAt(i);
                                    i++;
                                    setTimeout(typeWriter, speed);
                                }
                            }

                            typeWriter();
                        }
                        else {
                            alert('Generate fail!\nError: ' + content);
                        }
                    },
                    error: function (thrownError) {
                        // console.log("error msg:", thrownError);
                        alert("API fail!\nError: " + thrownError);
                    },
                    complete: function () {
                        $("#generate_button").prop('disabled', false);
                        $("#start-icon").show();
                        $("#loading-icon").hide();
                    }
                });
            }
            else {
                alert("Only .csv file!")
            }
        }
        else {
            alert("Please upload the badminton game data!")
        }
    });

    $("#reset_button").click(function () {
        init();
    })
}); 