$(function() {
    $('#btnSignUp').bind("click", function() {

        var errorMessage = "An Unknown Error Has Occured"

        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                document.write(response);
                $('#btnSignUp').unbind('submit').submit();
            },
            error: function(err, xhr) {
                $('#btnSignUp').unbind('submit').submit();

                if( $('.jumbotron span').length == 0 )
                {
                    var errorElement = document.createElement("span");
                    var strongElement = document.createElement("strong");
                    errorElement.append(strongElement);
                    var jumbotron = $(".jumbotron");
                    jumbotron.append(errorElement);
                }
                var errorTextNode = document.createTextNode(errorMessage);
                $(".jumbotron span strong").empty();
                $(".jumbotron span strong").append(errorTextNode);
            }
        });
    });
});
