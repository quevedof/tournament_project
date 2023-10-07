# tournament_project

The best tournament app in the world - with the best mango juice. 




POST `/api/create-tournament`

Request Body
```
{
    "name": "League of Legends",
    "number_of_teams": 2
}
```


POST `/api/join`

Request Body
```
{
    "email": "hello@world.com",
    "teamName": "Pikachu",
    "tournamentKey": "QlEFm51RcG"
}
```

GET `/api/tournaments/{tournamentKey}`

Response Body
```
{
    "id": 3,
    "name": "League of Legends",
    "generated_key": "QlEFm51RcG",
    "number_of_teams": 2,
    "date": "2023-10-07T17:06:14.437633Z"
}
```

