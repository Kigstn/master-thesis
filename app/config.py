use_case_base = [
    [
        [
            "float-md-end",
            "use_case_decoration",
        ],
        "Sie sind ein großer Fußballfan und freuen sich sehr auf die Europameisterschaft, welche in sieben Tagen beginnt. Zu diesem Anlass haben Sie sich mit Freunden bei sich zu Hause verabredet, um das Eröffnungsspiel live zu gucken. Sie freuen sich so sehr darauf, dass Sie schon jetzt, eine Woche vor dem Event, Ihr Haus dekoriert haben.",
        "Allerdings ist etwas passiert: Ihr Fernseher ist kaputt gegangen! Der Schaden ist irreparabel und Sie müssen jetzt innerhalb von einer Woche irgendwie Ersatz bekommen.",
    ],
]

use_case_1 = use_case_base + [
    "Der Fernseher war nur wenige Monate alt. Ohne das Sie etwas getan haben, gab es wie aus dem Nichts ein Knacken, der Fernseher ist ausgegangen und geht nun nicht mehr an.",
    "Sie gehen also auf die Website des lokalen Technikgeschäftes und bestellen online einen Fernseher. Der Fernseher soll direkt am nächsten Tag zugestellt werden, es gibt also theoretisch sechs Tage Buffer bis zum Eröffnungsspiel.",
    [
        [
            "float-md-start",
            "use_case_five_days_left",
        ],
        "Allerdings kommt weder die Versandbestätigung noch der Fernseher am nächsten Tag an. Am Tag danach rufen Sie also die Supporthotline des Ladens an und warten erst einmal 45 Minuten in der Warteschleife, bis Sie mit einem Mitarbeiter sprechen. Sie schildern dem Mitarbeiter Ihre Situation und der Mitarbeiter der Hotline sagt, dass Sie falschliegen. Der Fernseher sollte nie schon gestern ankommen, er soll aber zwei Tage vor dem Eröffnungsspiel zugestellt werden.",
    ],
    [
        [
            "float-md-end",
            "use_case_one_day_left",
        ],
        "Auch das stimmt aber nicht ganz. Einen Tag vor dem Spiel trifft die Versandbestätigung ein und der Fernseher wird noch am gleichen Tag zugestellt. Allerdings funktioniert der Fernseher nicht, obwohl er von außerhalb unbeschadet wirkt. Da Sie am Telefon so lange in der Warteschleife warten mussten und am nächsten Tag schon das Eröffnungsspiel ist, gehen Sie dieses Mal lieber zum Laden, um hoffentlich eine Lösung zu finden.",
    ],
    [
        [
            "float-md-start",
            "use_case_queue",
        ],
        "Im Laden angekommen hat nur einer der Serviceschalter offen und dieser hat eine sehr lange Schlange. Bis Sie dran sind, dauert es noch mal eine halbe Stunde.",
        "Als Sie dran bist, sagen Sie zu dem Mitarbeiter:",
    ],
    "Hallo. Mein Fernseher ist neulich kaputt gegangen. Deshalb habe ich letzte Woche bei diesem Laden online einen neuen Fernseher bestellt. Mir wurde gesagt, die Lieferung dauert nur einen Tag, es hat aber sechs Tage gedauert, bis der Fernseher überhaupt versendet worden ist. Der Fernseher ist außerdem kaputt angekommen. Ich habe Zeitdruck und bis morgen brauche ich unbedingt einen funktionierenden Fernseher!",
]
use_case_2 = use_case_base + [
    [
        [
            "float-md-start",
            "use_case_broken_tv",
        ],
        "Ihr 16-jähriges Kind hat am Wochenende, als Sie mit Ihrem Ehepartner bei Ihrer Mutter zu Besuch waren, ohne Ihr Wissen eine Hausparty mit vielen Gästen geschmissen. Die Party ist eskaliert - als Sie nach Hause kommst, riecht es immer noch überall nach Erbrochenem und Ihr Fernseher ist in Scherben. Irgendwer auf der Party hat ihn umgestoßen. Ihr Kind sagt Ihnen, dass keiner den Vorfall gesehen hat, der Täter ist unbekannt.",
    ],
    [
        [
            "float-md-end",
            "use_case_store",
        ],
        "Nachdem Sie die Situation gesehen haben, wird es Ihnen zu viel und Sie verlassen das Haus, um sich zu beruhigen. Weil Ihnen der kaputte Fernseher und das kommende Eröffnungsspiel die ganze Zeit im Kopf schweben, nutzen Sie die Gelegenheit und wollen gleich einen neuen Fernseher kaufen. Sie gehen also zum lokalem Technikgeschäft, um einen Fernseher zu kaufen.",
        "Dort angekommen gehen Sie zu einem Mitarbeiter und sagen:",
     ],
    "Hallo. Mein Fernseher ist gerade kaputt gegangen. Ich brauche bis in spätestens 7 Tagen einen funktionierenden Fernseher.",
]
use_case_3 = use_case_base + [
    [
        [
            "float-md-start",
            "use_case_store",
        ],
        "Der Fernseher war schon über 10 Jahre alt. Ohne dass Sie etwas getan haben, gab es wie aus dem Nichts es ein Knacken, der Fernseher ist ausgegangen und geht nun nicht mehr an. Sie wollten allerdings sowieso demnächst einen neuen Fernseher kaufen und sind deshalb von der Situation gar nicht frustriert. Sie sehen es als einen guten Zeitpunkt, sich endlich einen neuen Fernseher anzuschaffen. Sie gehen also zum lokalem Technikgeschäft, um einen Fernseher zu kaufen.",
    ],
    [
        [
            "float-md-end",
            "use_case_sale",
        ],
        "Im Laden angekommen gehen Sie zu einem Mitarbeiter, um sich beraten zu lassen. Der Mitarbeiter ist sehr freundlich und nimmt sich viel Zeit, Ihnen die Feinheiten von verschiedenen Fernsehern zu erklären. Außerdem schlägt der Mitarbeiter Ihnen vor, einen bestimmten Fernseher zu kaufen, weil dieser die besten Eigenschaften hat und zusätzlich gerade im Angebot ist. Der Mitarbeiter sagt Ihnen zudem, dass der Laden aktuell eine Aktion hat, wo Kunden beim Kauf eines Elektrogerätes auf Wunsch eine kostenlose Lieferung, Montage und Einrichtung des Gerätes bekommen. Das alte Gerät kann dann außerdem gleich mitgenommen werden. Für Sie kommt das genau richtig, da ein Fernseher keineswegs in Ihr kleines Auto passen wird.",
        "Sie fühlen sich wirklich sehr gut beraten und haben vor, den Ihnen empfohlenen Fernseher zu kaufen. Der Mitarbeiter verweißt Sie für den Kauf auf einen zuständigen Kollegen.",
    ],
    "Sie gehen also zu dem Mitarbeiter und sagen:",
    "Hallo. Mein Fernseher ist gerade kaputt gegangen. Ich brauche bis in spätestens 7 Tagen einen funktionierenden Fernseher. Ich möchte gerne diesen bestimmten Fernseher (Du zeigst auf den gewünschten Fernseher).",
]
use_case_4 = use_case_base + [
    [
        [
            "float-md-start",
            "use_case_you_won",
        ],
        "Der Fernseher war schon über 10 Jahre alt. Ohne dass Sie etwas getan hast, gab es wie aus dem Nichts ein Knacken, der Fernseher ist ausgegangen und geht nun nicht mehr an. Sie wollten allerdings sowieso demnächst einen neuen Fernseher kaufen und sind deshalb von der Situation gar nicht frustriert. Sie sehen es als einen guten Zeitpunkt, sich endlich einen neuen Fernseher anzuschaffen und wissen auch schon genau, welches Modell Sie kaufen wollen. Sie nehmen sich vor, am nächsten Tag loszugehen, um den Fernseher zu ersetzen.",
        "Bevor Sie am Tag danach losgehen, bekommen Sie eine E-Mail und stellen fest, dass Sie eine Lotterie deiner Stadt über einen Gutschein von 500€ gewonnen haben! Sie hatten schon vor Wochen an der Lotterie teilgenommen und sie schon ganz vergessen. Die Lotterie wurde von der Stadt ausgetragen, um lokale Geschäfte in Zeiten des Internetverkaufes zu stärken und der Gutschein, den Sie gewonnen haben, ist in jedem Geschäft deiner Stadt gültig. Sie verbinden also die beiden Aktionen und machen sich auf den Weg zum lokalem Technikgeschäft, um einen Fernseher zu kaufen. Sie wissen außerdem, dass dort genau der Fernseher vorrätig ist, welchen Sie kaufen wollen.",
    ],
    [
        [
            "float-md-end",
            "use_case_store",
        ],
        "Im Laden angekommen gehen Sie zu einem Mitarbeiter, um den Fernseher zu kaufen und sagen:",
    ],
    "Hallo. Mein Fernseher ist gerade kaputt gegangen. Ich brauche bis in spätestens 7 Tagen einen funktionierenden Fernseher. Ich möchte gerne diesen bestimmten Fernseher (Du zeigst auf den gewünschten Fernseher). Ich habe außerdem einen Gutschein, welchen ich gerne einlösen möchte.",
]

use_case_dict = {
    1: use_case_1,
    2: use_case_2,
    3: use_case_3,
    4: use_case_4,
}

emotions_dict = [
    {
        "anger": {
            "style": "btn-outline-danger",
            "image": "/anger.png",
            "labels": [
                "Wütend / Frustriert",
                "Englisch: Angry",
            ],
        },
        "embarrassment": {
            "style": "btn-outline-warning",
            "image": "/embarrassment.png",
            "labels": [
                "Verlegen / Beschämt",
                "Englisch: Embarrassed",
            ],
        },
        "happiness": {
            "style": "btn-outline-success",
            "image": "/happiness.png",
            "labels": [
                "Glücklich / Freudig",
                "Englisch: Happy",
            ],
        },
    },
    {
        "sadness": {
            "style": "btn-outline-purple",
            "image": "/sadness.png",
            "labels": [
                "Traurig / Müde",
                "Englisch: Sad",
            ],
        },
        "anxiety": {
            "style": "btn-outline-secondary",
            "image": "/anxiety.png",
            "labels": [
                "Besorgt / Unwohl",
                "Englisch: Anxious",
            ],
        },
        "relaxedness": {
            "style": "btn-outline-info",
            "image": "/relaxedness.png",
            "labels": [
                "Entspannt / Gelassen",
                "Englisch: Relaxed",
            ],
        },
    },
]

limesurvey_user_info_url = "https://limesurvey.rz.tu-bs.de/index.php/492768"
limesurvey_use_case_evaluation = "https://limesurvey.rz.tu-bs.de/index.php/742517"
limesurvey_interface_evaluation = "https://limesurvey.rz.tu-bs.de/index.php/351253"

experiment_steps = 3
