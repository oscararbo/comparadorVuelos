# AMADEUS API INTEGRATION GUIDE

## Overview
This guide explains how the Amadeus Flight Search API is integrated into the flight comparison application.

## Authentication Flow

### OAuth2 Client Credentials Grant
The application uses OAuth2 with client credentials to authenticate with Amadeus:

```
1. POST /v1/security/oauth2/token
   - Client ID: Your API Key
   - Client Secret: Your API Secret
   - Grant Type: client_credentials

2. Response: Access Token + Expiry Time

3. Use Bearer Token for subsequent requests
```

### Token Caching
- The access token is cached in memory to avoid unnecessary authentication calls
- Automatically refreshes 1 minute before expiry (default 30-minute validity)
- Transparent to the user

## Flight Search Endpoint

### Endpoint
```
GET https://api.amadeus.com/v2/shopping/flight-offers
```

### Required Parameters
- `originLocationCode`: IATA code of departure airport (e.g., "MAD")
- `destinationLocationCode`: IATA code of arrival airport (e.g., "CDG")
- `departureDate`: Departure date in YYYY-MM-DD format
- `adults`: Number of adult passengers

### Optional Parameters
- `returnDate`: Return date for round-trip flights (YYYY-MM-DD format)
- `max`: Maximum number of flight offers to return (default: 10, max: 250)

### Response Format
```json
{
  "data": [
    {
      "price": {
        "total": "1234.56",
        "currency": "EUR"
      },
      "itineraries": [
        {
          "duration": "PT2H15M",
          "segments": [
            {
              "departure": {
                "iataCode": "MAD",
                "at": "2024-12-25T10:30:00"
              },
              "arrival": {
                "iataCode": "CDG",
                "at": "2024-12-25T12:45:00"
              },
              "carrierCode": "IB",
              "number": "6840",
              "aircraft": {"code": "32N"}
            }
          ]
        }
      ],
      "travelerPricings": [...]
    }
  ]
}
```

## Data Handling

### Formatting Flight Results
The application formats Amadeus API responses into human-readable format:

1. **Price Information**
   - Total price in EUR
   - Currency code

2. **Itinerary Details**
   - Total duration (e.g., "2h 15m")
   - Departure and arrival times
   - Departure and arrival airports

3. **Segment Information**
   - Airline code and flight number
   - Aircraft type
   - Departure/arrival times for each leg

### CSV Storage
Search results are automatically saved to `historico_precios.csv` with the following fields:
- Origen (Origin)
- Destino (Destination)
- Fecha Salida (Departure Date)
- Fecha Regreso (Return Date)
- Precio Mínimo (Minimum Price)
- Moneda (Currency)
- Timestamp

## Error Handling

### Common Errors

#### 401 Unauthorized
- **Cause**: Invalid API Key or API Secret
- **Solution**: Verify credentials in `api_handler.py`

#### 400 Invalid Location Codes
```json
{
  "errors": [
    {
      "status": 400,
      "code": "INVALID_FORMAT",
      "detail": "The location code is not valid"
    }
  ]
}
```
- **Cause**: Non-existent IATA code
- **Solution**: Use valid 3-letter IATA airport codes

#### 400 Invalid Date
```json
{
  "errors": [
    {
      "status": 400,
      "code": "INVALID_FORMAT",
      "detail": "Invalid date format"
    }
  ]
}
```
- **Cause**: Incorrect date format or past date
- **Solution**: Use YYYY-MM-DD format and ensure date is in the future

#### 404 No Flight Offers
- **Cause**: No flights available for the specified route and dates
- **Solution**: Try different airports or dates

## Rate Limiting

### Quotas
- **Test Environment**: Limited API calls per month (check your Amadeus dashboard)
- **Production**: Based on subscription tier

### Best Practices
1. Cache results when possible
2. Avoid making duplicate searches immediately
3. Use appropriate time intervals between searches
4. Monitor your API usage in the Amadeus dashboard

## IATA Airport Codes

### Spain
- MAD: Madrid-Barajas
- BCN: Barcelona-El Prat
- SVQ: Seville
- ALC: Alicante-Elche
- VLC: Valencia
- BIO: Bilbao
- AGP: Málaga-Costa del Sol
- IBZ: Ibiza
- PMI: Palma de Mallorca
- TFS: Tenerife South
- TFN: Tenerife North

### Europe
- CDG: Paris-Charles de Gaulle
- LHR: London-Heathrow
- AMS: Amsterdam-Schiphol
- FCO: Rome-Fiumicino
- DUB: Dublin
- ZRH: Zurich
- VIE: Vienna
- PRG: Prague
- MUC: Munich

## Configuration

### Environment Variables (Optional)
For added security, you can use environment variables instead of hardcoding:

```python
import os

API_KEY = os.getenv("AMADEUS_API_KEY", "YOUR_API_KEY_HERE")
API_SECRET = os.getenv("AMADEUS_API_SECRET", "YOUR_API_SECRET_HERE")
```

Set environment variables:
```bash
# Windows PowerShell
$env:AMADEUS_API_KEY = "your-key-here"
$env:AMADEUS_API_SECRET = "your-secret-here"

# Windows Command Prompt
set AMADEUS_API_KEY=your-key-here
set AMADEUS_API_SECRET=your-secret-here

# Linux/macOS
export AMADEUS_API_KEY="your-key-here"
export AMADEUS_API_SECRET="your-secret-here"
```

## Useful Links

- [Amadeus Flight Offers Search API](https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search)
- [Amadeus Developer Dashboard](https://developers.amadeus.com/my-apps)
- [IATA Airport Codes](https://www.iata.org/en/publications/directories/code-search/)
- [REST API Testing with Postman](https://www.postman.com/amadeus4dev/)

## Troubleshooting

### "No access token returned"
- Check internet connection
- Verify API credentials
- Check Amadeus API status page

### Inconsistent Results
- Results vary based on real-time availability
- Different times of day may yield different results
- Prices are dynamic and change frequently

### Performance Issues
- Amadeus API typically responds in 500ms-2s
- Network latency affects overall response time
- Consider implementing a loading indicator (already done in GUI)

## Future Enhancements

Potential improvements:
1. Multi-city flight searches
2. Seat availability check
3. Price history and trend analysis
4. Flight price alerts
5. Integration with booking APIs
6. Support for different currencies
7. Advanced filtering options
8. Real-time price comparison with other providers