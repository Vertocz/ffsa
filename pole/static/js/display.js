// Variables globales pour les scores et le temps de match
let matchTime = 10 * 60;  // 10 minutes en secondes
let matchMilliseconds = 0;  // Millisecondes du chrono
let possessionTime = 12;  // Temps de possession en secondes
let possessionMilliseconds = 0;  // Millisecondes pour la possession





let matchId = "match1"; // L'identifiant du match à afficher
const displaySocket = new WebSocket(`ws://127.0.0.1:8000/ws/match/${matchId}/`);

// Écouter les messages
displaySocket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.type === "score") {
        const teamScore = document.getElementById(`${data.team}-score`);
        teamScore.textContent = data.points;
    }
};

// Gestion des erreurs et de la connexion
displaySocket.onopen = function() {
    console.log("WebSocket connecté au match " + matchId);
};

displaySocket.onclose = function() {
    console.log("WebSocket déconnecté");
};





// Fonction pour ajuster les couleurs des fautes
function updateFoulsColor(team) {
    const teamFoulsElement = document.getElementById(team + '-fouls');
    let currentFouls = parseInt(teamFoulsElement.textContent.replace('Fautes: ', ''));

    if (currentFouls < 6) {
        teamFoulsElement.classList.remove("orange", "red", "violet");
        teamFoulsElement.classList.add("green");
    } else if (currentFouls < 7) {
        teamFoulsElement.classList.remove("green", "red", "violet");
        teamFoulsElement.classList.add("orange");
    } else if (currentFouls < 10) {
        teamFoulsElement.classList.remove("green", "orange", "violet");
        teamFoulsElement.classList.add("red");
    } else {
        teamFoulsElement.classList.remove("green", "orange", "red");
        teamFoulsElement.classList.add("violet");
    }
}

// Fonction pour mettre à jour le chrono du match
function runMatchTime() {
    if (matchMilliseconds === 0) {
        if (matchTime > 0) {
            matchTime--;  // Décrémenter une seconde
        }
        matchMilliseconds = 9;  // Réinitialiser les millisecondes
    } else {
        matchMilliseconds--;  // Décrémenter les millisecondes
    }

    // Format du chrono du match (min:sec.ms)
    const minutes = Math.floor(matchTime / 60);
    const seconds = matchTime % 60;
    document.getElementById("match-time").textContent = `${minutes}:${seconds < 10 ? '0' + seconds : seconds}.${matchMilliseconds}`;
}

// Fonction pour mettre à jour le temps de possession
function runPossessionTime() {
    if (possessionMilliseconds === 0) {
        if (possessionTime > 0) {
            possessionTime--;  // Décrémenter une seconde
        }
        possessionMilliseconds = 9;  // Réinitialiser les millisecondes
    } else {
        possessionMilliseconds--;  // Décrémenter les millisecondes
    }

    // Format du temps de possession (sec.ms)
    document.getElementById("possession-time").textContent = `${possessionTime}.${possessionMilliseconds}`;

    // Mise à jour de la barre de possession
    const possessionBar = document.getElementById("possession-bar");
    const height = (possessionTime / 12) * 100;  // Échelle du temps de possession
    possessionBar.style.height = `${height}%`;

    // Changement de couleur de la barre de possession
    if (possessionTime <= 3) {
        possessionBar.style.backgroundColor = "#e26e00";  // Orange dans les 3 dernières secondes
    } else if (possessionTime <= 0) {
        possessionBar.style.backgroundColor = "transparent";  // Transparent quand à 0
    } else {
        possessionBar.style.backgroundColor = "#008819";  // Retour à la couleur initiale (verte)
    }
}

// Initialisation du fond d'écran et des autres éléments
function updateBackground() {
    const background = document.getElementById("background");
    const remainingTime = matchTime + matchMilliseconds / 10;
    const totalTime = 10 * 60;

    // Mise à jour de l'affichage sans fond dynamique
    if (remainingTime / totalTime < 0.5) {
        document.body.style.color = "#fff";
        document.getElementById("match-time").style.color = "#fff";
        document.getElementById("possession-time").style.color = "#fff";
    } else {
        document.body.style.color = "#000";
        document.getElementById("match-time").style.color = "#000";
        document.getElementById("possession-time").style.color = "#000";
    }
}

// Fonction pour démarrer le match
function startMatch() {
    setInterval(() => {
        runMatchTime();
        updateBackground();
    }, 100);  // Met à jour toutes les 100ms (dixièmes de seconde)

    setInterval(runPossessionTime, 100);  // Met à jour le chrono de possession
}

startMatch();
