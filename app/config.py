use_case_base = [
    [
        [
            "float-md-end",
            "use_case_decoration",
        ],
        "Du bist ein großer Fußballfan und freust dich sehr auf die Europameisterschaft, welche in sieben Tagen beginnt. Zu diesem Anlass hast du dich mit Freunden bei dir zu Hause verabredet, um das Eröffnungsspiel live zu gucken. Du freust dich so sehr darauf, dass du schon jetzt, eine Woche vor dem Event dein Haus dekoriert hast.",
        "Allerdings ist etwas passiert: Dein Fernseher ist kaputt gegangen! Der Schaden ist irreparabel und du musst jetzt innerhalb von einer Woche irgendwie Ersatz bekommen",
    ],
]

use_case_1 = use_case_base + [
    "Der Fernseher war nur wenige Monate alt. Ohne das du etwas getan hast, gab es wie aus dem Nichts es ein Knacken, der Fernseher ist ausgegangen und geht nun nicht mehr an.",
    "Du gehst also auf die Website des lokalen Technikgeschäftes und bestellst online einen Fernseher. Der Fernseher soll direkt am nächsten Tag zugestellt werden, es gibt also theoretisch sechs Tage Buffer bis zum Eröffnungsspiel.",
    [
        [
            "float-md-start",
            "use_case_five_days_left",
        ],
        "Allerdings kommt weder die Versandbestätigung noch der Fernseher am nächsten Tag an. Am Tag danach rufst du also die Supporthotline des Ladens an und wartest erst einmal 45 Minuten in der Warteschleife, bis du mit einem Mitarbeiter sprichst. Du schilderst dem Mitarbeiter deine Situation und der Mitarbeiter der Hotline sagt, dass du falschliegst. Der Fernseher sollte nie schon gestern ankommen, er soll aber zwei Tage vor dem Eröffnungsspiel zugestellt werden.",
    ],
    [
        [
            "float-md-end",
            "use_case_one_day_left",
        ],
        "Auch das stimmt aber nicht ganz. Einen Tag vor dem Spiel trifft die Versandbestätigung ein und der Fernseher wird noch am gleichen Tag zugestellt. Allerdings funktioniert der Fernseher nicht, obwohl er von außerhalb unbeschadet wirkt. Da du am Telefon so lange in der Warteschleife warten musstest und am nächsten Tag schon das Eröffnungsspiel ist, gehst du dieses Mal lieber zum Laden, um hoffentlich eine Lösung zu finden.",
    ],
    [
        [
            "float-md-start",
            "use_case_queue",
        ],
        "Im Laden angekommen hat nur eine Kasse offen und die hat eine sehr lange Schlange. Bis du dran bist, dauert es noch mal eine halbe Stunde.",
        "Als du dran bist, sagst du zu dem Mitarbeiter:",
    ],
    "Hallo. Mein Fernseher ist neulich kaputt gegangen. Deshalb habe ich letzte Woche bei diesem Laden online einen neuen Fernseher bestellt. Mir wurde gesagt, die Lieferung dauert nur einen Tag, es hat aber sechs Tage gedauert, bis der Fernseher überhaupt versendet worden ist. Der Fernseher ist außerdem kaputt angekommen. Ich habe Zeitdruck und bis morgen brauche ich unbedingt einen funktionierenden Fernseher!",
]
use_case_2 = use_case_base + [
    [
        [
            "float-md-start",
            "use_case_broken_tv",
        ],
        "Dein 16-jähriges Kind hat am Wochenende, als du mit deinem Ehepartner bei deiner Mutter zu Besuch warst, ohne dein Wissen eine Hausparty mit vielen Gästen geschmissen. Die Party ist eskaliert - als du nach Hause kommst, riecht es immer noch überall nach Erbrochenem und dein Fernseher ist in Scherben. Irgendwer auf der Party hat ihn umgestoßen. Dein Kind sagt dir, dass keiner den Vorfall gesehen hat, der Täter ist unbekannt.",
    ],
    [
        [
            "float-md-end",
            "use_case_store",
        ],
        "Nachdem du die Situation gesehen hast, wird es dir zu viel und du verlässt das Haus, um dich zu beruhigen. Weil dir der kaputte Fernseher und das kommende Eröffnungsspiel die ganze Zeit im Kopf schweben, nutzt du die Gelegenheit und willst gleich einen neuen Fernseher kaufen. Du gehst also zum lokalem Technikgeschäft um einen Fernseher zu kaufen.",
        "Dort angekommen gehst du zu einem Mitarbeiter und sagst:",
     ],
    "Hallo. Mein Fernseher ist gerade kaputt gegangen. Ich brauche bis in spätestens 7 Tagen einen funktionierenden Fernseher.",
]
use_case_3 = use_case_base + [
    [
        [
            "float-md-start",
            "use_case_store",
        ],
        "Der Fernseher war schon über 20 Jahre alt. Ohne dass du etwas getan hast, gab es wie aus dem Nichts es ein Knacken, der Fernseher ist ausgegangen und geht nun nicht mehr an. Du wolltest allerdings sowieso demnächst einen neuen Fernseher kaufen und bist deshalb von der Situation gar nicht frustriert. Du siehst es als einen guten Zeitpunkt, dir endlich einen neuen Fernseher anzuschaffen. Du gehst also zum lokalem Technikgeschäft um einen Fernseher zu kaufen.",
    ],
    [
        [
            "float-md-end",
            "use_case_sale",
        ],
        "Im Laden angekommen gehst du zu einem Mitarbeiter, um dich beraten zu lassen. Der Mitarbeiter ist sehr freundlich und nimmt sich viel Zeit, dir die Feinheiten von verschiedenen Fernsehern zu erklären. Außerdem schlägt der Mitarbeiter dir vor, einen bestimmten Fernseher zu kaufen, weil dieser die besten Eigenschaften hat und zusätzlich gerade im Angebot ist. Der Mitarbeiter sagt dir zudem, dass der Laden aktuell eine Aktion hat, wo Kunden beim Kauf eines Elektrogerätes das alte, eventuell kaputte Elektrogerät abgeben können. Der Laden kümmert sich dann um die korrekte Entsorgung oder eine eventuelle Reparatur und anschließenden Weiterverkauf und die Kunden bekommen dafür einen zusätzlichen Rabatt.",
        "Du fühlst dich sehr gut beraten und hast vor, den dir empfohlenen Fernseher zu kaufen. Du findest außerdem, dass der Fernseher einen sehr, sehr guten Preis hat und sich super für dich eignet. Weiterhin findest du, dass der Mitarbeiter sich deutlich mehr als nötig um dich gekümmert hat und das, obwohl der Laden voll ist und er bestimmt auch andere Sachen zu tun hat. Du gehst also zur Kasse, um den Fernseher zu kaufen. Es haben mehrere Kassen offen, du musst also nicht warten.",
    ],
    "Bei der Kasse angekommen sagst du:",
    "Hallo. Mein Fernseher ist gerade kaputt gegangen. Ich brauche bis in spätestens 7 Tagen einen funktionierenden Fernseher. Ich möchte gerne diesen bestimmten Fernseher (Du zeigst auf den gewünschten Fernseher).",
]
use_case_4 = use_case_base + [
    [
        [
            "float-md-start",
            "use_case_you_won",
        ],
        "Der Fernseher war schon über 20 Jahre alt. Ohne dass du etwas getan hast, gab es wie aus dem Nichts es ein Knacken, der Fernseher ist ausgegangen und geht nun nicht mehr an. Du wolltest allerdings sowieso demnächst einen neuen Fernseher kaufen und bist deshalb von der Situation gar nicht frustriert. Du siehst es als einen guten Zeitpunkt, dir endlich einen neuen Fernseher anzuschaffen und weißt auch schon genau, welches Modell du kaufen willst. Du nimmst dir vor, am nächsten Tag loszugehen, um den Fernseher zu ersetzen.",
        "Bevor du am Tag danach losgehst, bekommst du eine E-Mail und stellst fest, dass du eine Lotterie deiner Stadt über einen Gutschein von 500€ gewonnen hast! Du hattest schon vor Wochen an der Lotterie teilgenommen und sie schon ganz vergessen. Die Lotterie wurde von der Stadt ausgetragen, um lokale Geschäfte in Zeiten des Internetverkaufes zu stärken und der Gutschein, den du gewonnen hast, ist in jedem Geschäft deiner Stadt gültig. Du verbindest also die beiden Aktionen und machst dich auf den Weg zum lokalem Technikgeschäft um einen Fernseher zu kaufen. Du weißt außerdem, dass sie dort genau den Fernseher haben, welchen du kaufen willst.",
    ],
    [
        [
            "float-md-end",
            "use_case_store",
        ],
        "Im Laden angekommen gehst du zur Kasse, um den Fernseher zu kaufen und sagst zu dem Mitarbeiter:",
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
