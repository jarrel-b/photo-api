# photo-api
Documentation for photo-api.
## Installation
This project requires python version 3.7.

Install the requirements via pip:
```
pip install -r requirements-dev.txt
```
Verify the installation via the command:
```
make test
```
The server can be started on port `8000` via:
```
make run-local
```
## Endpoints
### `GET /v1/catalog` 
This endpoint list the available photos for purchase.
###### EXAMPLE REQUEST
```
curl -X GET localhost:8000/v1/catalog
```
###### RESPONSE (STATUS 200)
###### Response Content Type (application/json)
```
{
  "count": 1,
  "last_token": 11,
  "results": [
    {
      "id": 11,
      "title": "Photo0",
      "location": "New York",
      "year": 1992,
      "path": "path/to/photo11.png"
    }
  ]
}
```
###### REQUEST PARAMETERS
|Parameter|Description|Example|
|---|---|---|
|page_size|Length of page|20
|last_token|Last `id` evaluated from previous call|20
### `POST /v1/checkout`
This endpoint handles a purchasing of a print.
###### EXAMPLE REQUEST
```
curl -X POST -H "Content-Type: application/json" localhost:8000/v1/catalog \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@domain.com",
    "address_line_one": "P Sherman 42 Wallaby Way",
    "address_line_two": "Apartment 1",
    "city": "Sydney",
    "state_or_region": "New South Wales",
    "postal_code": 2000,
    "print_id": 1,
    "photo_id": 10
  }'
```
###### REQUEST PARAMETERS
|Parameter|Description|
|---|---|
|first_name|First name|
|last_name|Last name|
|email|Email address to send order confirmation to|
|address_line_one|Address to ship to|
|address_line_two|Second address line|
|city|City|
|state_or_region|State or region|
|postal_code|Postal code|
|print_id|`id` of requested print size|
|photo_id|`id` of requested photo|
###### RESPONSE (STATUS 201)
###### Response Content Type (application/json)
```
{
  "id": "b3911e8d-829f-491a-b03f-f535181440d6",
  "status": "created",
  "placed_on": "2020-01-01T12:23:45",
  "items_ordered": [
    {
      "title": "Photo0",
      "size": "med"
    }
  ],
  "shipping_summary": {
    "ship_to": "John Smith",
    "email": "john.smith@domain.com",
    "phone": "555-555-5555",
    "address": "P Sherman 42 Wallaby Way Apartment 1",
    "city": "Sydney",
    "state_or_region": "New South Wales",
    "postal_code": 2000,
    "country": "AUS"
  },
  "billing_summary": {
    "order_total": 20.99,
    "shipping_total": 5.99,
    "item_total": 15
  }
}
```
###### RESPONSE (STATUS 415)
###### Response Content Type (text/html)
```
Response: 415 Unsupported Media Type
```
###### RESPONSE (STATUS 422)
###### Response Content Type (application/json)
```
{
  "first_name": ["This field is required."],
  "last_name": ["This field is required."]
}
```
### `GET /v1/checkout/print-sizes`
This endpoint lists available print sizes.
###### EXAMPLE REQUEST
```
curl -X GET localhost:8000/v1/checkout/print-sizes
```
###### RESPONSE (STATUS 200)
###### Response Content Type (application/json)
```
{
  "1": "sml",
  "2": "med",
  "3": "lrg"
}
```
