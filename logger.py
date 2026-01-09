"""
Only does:
	•	Write structured logs (CSV or JSON)
	•	Never blocks the main loop

Greenhouse soil moisture sensor interface.

Reads soil moisture via ADC and returns normalized values.
"""