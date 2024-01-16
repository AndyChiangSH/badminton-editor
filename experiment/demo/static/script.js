$(function () {
    var typing = false;
    var copy_text = "";
    var file_name = "";

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
        file_name = file["name"].split(".")[0];
        let model = $('#input_model').val();
        // console.log("file:", file)
        // console.log("model:", model)

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
                        // console.log("response:", response)
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
                            copy_text = content

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
                        alert("API ERROR!\nPlease let us know, and we will fix it as soon as possible.");
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

    $("#copy-to-clipboard").click(function () {
        navigator.clipboard.writeText(copy_text).then(function () {
            alert("Copy to clipboard successful.");
        }, function (err) {
            alert("Copy to clipboard fail!");
        });
    })

    $("#download-txt").click(function () {
        // console.log("download txt");
        // console.log(this);
        this.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(copy_text));
        this.setAttribute('download', file_name + ".txt");
    })
}); 