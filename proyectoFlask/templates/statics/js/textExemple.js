$("#name-button").click(function(event){
    let message = {
        name: $("#text-input").val()
    }
    $.post("http://10.0.0.4:5000/hello", JSON.stringify(message),
        function (response) {
            $("#get-name").text(response.greeting);
            console.log(response);
        });
});