# tournament_project

The best tournament app in the world - with the best mango juice. 


### Create Tournament
POST `/api/create-tournament`

Request Body
```
{
    "name": "League of Legends",
    "numberOfTeams": 2
}
```
Response Body
```
{
    "name": "League of Legends",
    "numberOfTeams": 2.0,
    "generatedKey": "bHcv1Qb2hP",
    "date": "2023-10-07T21:31:42.007740"
}
```

### Join Tournament
POST `/api/join`

Request Body
```
{
    "email": "hello@world.com",
    "teamName": "Pikachu",
    "tournamentKey": "QlEFm51RcG"
}
```


### Get Tournament Details by Key
GET `/api/tournaments/{tournamentKey}`

Response Body
```
{
    "id": 11,
    "name": "League of Legends",
    "generatedKey": "bHcv1Qb2hP",
    "numberOfTeams": 2,
    "date": "2023-10-07T21:31:42.007740Z"
}
```

### Get Tournament Overall Details by key (includes matches, match participants, scores)
GET `/api/tournamenets/{tournamentKey}/overall`

Response Body
```
{
    "id": 1,
    "name": "Little League",
    "generatedKey": "Ayz7itPP0a",
    "matches": [
        {
            "id": 1,
            "date": "2023-10-07T22:41:48Z",
            "participants": [
                {
                    "id": 1,
                    "teamName": "mango team",
                    "score": 12
                }
            ],
            "winner": null,
            "nextMatchId": null
        }
    ]
}
```