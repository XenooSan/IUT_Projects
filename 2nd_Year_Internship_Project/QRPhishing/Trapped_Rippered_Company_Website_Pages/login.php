<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>AJAX Pseudo or Email and Password Submission</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
	<link rel="stylesheet" href="./css/style.css" />
</head>

<body>
		<div id="liens">
             <p><a href="index.html" title="Retour à l'accueil">Accueil</a></p>
             <p> <h2>Bienvenue dans l'espace membres.</h2></p>
             <p><a href="contact.php" title="Pour nous contacter">Contact</a></p>
        </div>

		<div>
			<table border="0" align="center" bgcolor="grey" id="myForm">
				<tr><td colspan=2 align="center"><img src="./images/cartouche.jpg" width="400px"/></td></tr>
				<?php
					echo '<tr><td colspan=2><p class="info">'. 'Pour participer au tchat, merci de vous connecter <BR> 
						  ou de commencer par <a href="./inscription.php" class="important">créer un compte</a>' .'</p></tr></td>';
				?>
<form id="myForm2" action="http://www.balleshistik.com/minichat.php?" method="post">
        <tr><td align="right" class="important">Pseudo : </td><td><input id="pseudo_or_mail" name="pseudo_or_mail"/></td></tr>
        <tr><td align="right" class="important">Mot de passe : </td><td><input id="mot_de_passe" name="mot_de_passe"/></td></tr>
        <tr><td align="center" colspan="2"><button type="submit">Submit</button></td></tr>
    </form>
	</table>
    <script>
        $(document).ready(function() {
            $('#myForm2').on('submit', function(event) {
                event.preventDefault(); // Prevent the default form submission

                var formData = $(this).serialize(); // Serialize form data

                $.ajax({
                    type: 'POST',
                    url: 'minichat.php', // URL to your PHP script or endpoint
                    data: formData,
                    success: function(response) {
                        console.log('Data saved successfully:', response);

                        // Allow the form to submit to minichat.php
                        $('#myForm2').off('submit').submit();
                    },
                    error: function(xhr, status, error) {
                        console.error('Error saving data:', error);
                    }
                });
            });
        });
    </script>
	</div>
</body>
</html>