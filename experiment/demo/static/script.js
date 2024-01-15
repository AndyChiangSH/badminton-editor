$(function () {
    var typing = false;

    function init() {
        $("#news").hide();
        $("#reset_button").hide();
        $("#generate_button").show();
        $("#news_content").html("");
        typing = false;
    }
    init();

    $("#generate_button").click(function () {
        var files = $('#input_file')[0].files[0];
        console.log("files:", files)

        if (files != undefined){
            if (files["type"] == "text/csv") {
                var fd = new FormData();
                fd.append('file', files);

                $.ajax({
                    url: '/pipeline',
                    type: 'post',
                    data: fd,
                    contentType: "application/json;",
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