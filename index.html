<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>wttr.in mit Koordinaten</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
        }
        /* Responsives Design für das iframe */
        .iframe-container {
            position: relative;
            overflow: hidden;
            padding-top: 100%; /* Verhältnis 1:1, anpassbar */
        }
        .iframe-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }
        /* Zentriertes Layout für Mobilgeräte */
        @media (min-width: 640px) {
            .container {
                max-width: 640px;
            }
        }
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">
    <div class="container mx-auto bg-white rounded-xl shadow-lg p-6 w-full max-w-xl">
        <h1 class="text-2xl font-bold text-gray-800 mb-4 text-center">Wetter von wttr.in mit Koordinaten</h1>
        <p class="text-gray-600 mb-6 text-center">
            Klicke auf den Button, um deine Koordinaten zu ermitteln und das Wetter für deinen aktuellen Standort anzuzeigen.
        </p>

        <button id="getWeatherBtn" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-4 rounded-xl shadow-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
            Wetter anzeigen
        </button>

        <div id="weatherContainer" class="mt-8 hidden">
            <h2 class="text-xl font-semibold text-gray-700 mb-4 text-center">Aktuelles Wetter</h2>
            <div id="weatherIframeWrapper" class="flex justify-center">
                <!-- Wetter-iFrame wird hier eingefügt -->
            </div>
        </div>

        <div id="messageBox" class="mt-8 text-center text-sm font-medium text-gray-500 hidden">
            <!-- Nachrichten wie Ladezustand oder Fehler werden hier angezeigt -->
        </div>
    </div>

    <script>
        const weatherBtn = document.getElementById('getWeatherBtn');
        const weatherContainer = document.getElementById('weatherContainer');
        const weatherIframeWrapper = document.getElementById('weatherIframeWrapper');
        const messageBox = document.getElementById('messageBox');

        // Funktion zur Anzeige von Nachrichten
        function showMessage(text, color = 'text-gray-500') {
            messageBox.textContent = text;
            messageBox.className = `mt-8 text-center text-sm font-medium ${color}`;
            messageBox.classList.remove('hidden');
        }

        // Klick-Event-Listener für den Button
        weatherBtn.addEventListener('click', () => {
            // Zeige Ladezustand an und verstecke vorherige Inhalte
            showMessage('Standort wird ermittelt...', 'text-blue-600');
            weatherContainer.classList.add('hidden');
            weatherBtn.disabled = true;

            // Prüfe, ob der Browser Geolocation unterstützt
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const lat = position.coords.latitude.toFixed(2);
                        const lon = position.coords.longitude.toFixed(2);
                        
                        // wttr.in URL mit den Koordinaten erstellen
                        // Die Formatierung `~lat,lon` ist der Standard für Koordinaten bei wttr.in
                        const weatherUrl = `https://wttr.in/~${lat},${lon}`;
                        
                        showMessage('Wetterdaten werden geladen...', 'text-green-600');
                        
                        // Erstelle ein `iframe` und füge es in den Wrapper ein
                        const iframe = document.createElement('iframe');
                        iframe.src = weatherUrl;
                        iframe.title = 'Wetter von wttr.in';
                        iframe.className = "w-full min-h-[400px]"; // Festgelegte Mindesthöhe für bessere Darstellung
                        iframe.onload = () => {
                            // Verstecke die Nachricht, wenn der iFrame geladen ist
                            messageBox.classList.add('hidden');
                            weatherContainer.classList.remove('hidden');
                            weatherBtn.disabled = false;
                        };
                        
                        // Leere den Wrapper und füge den neuen iFrame ein
                        weatherIframeWrapper.innerHTML = '';
                        weatherIframeWrapper.appendChild(iframe);
                    },
                    (error) => {
                        let errorMessage = 'Standort konnte nicht ermittelt werden.';
                        switch(error.code) {
                            case error.PERMISSION_DENIED:
                                errorMessage = 'Der Zugriff auf den Standort wurde verweigert.';
                                break;
                            case error.POSITION_UNAVAILABLE:
                                errorMessage = 'Standortinformationen sind nicht verfügbar.';
                                break;
                            case error.TIMEOUT:
                                errorMessage = 'Die Standortanfrage ist abgelaufen.';
                                break;
                        }
                        showMessage(`Fehler: ${errorMessage}`, 'text-red-600');
                        weatherBtn.disabled = false;
                    }
                );
            } else {
                // Browser unterstützt Geolocation nicht
                showMessage('Dein Browser unterstützt keine Geolocation.', 'text-red-600');
                weatherBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
