from datetime import datetime

START_DATE = "2025-01-01"
END_DATE = "2025-03-30"

START_FMT = datetime.strptime(START_DATE, "%Y-%m-%d").strftime("%Y%m%d")
END_FMT = datetime.strptime(END_DATE, "%Y-%m-%d").strftime("%Y%m%d")

BASE_URL = "https://pncp.gov.br/api/consulta/v1/contratos"
SIM_API_URL = "http://sim-api:8000/similarity"
