# Import Neccesary Libraries
import aiosqlite

class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_tfr(
        self, company_name: str, rocket_name: str, date: str, time_utc: str, area: str, reason: str
    ) -> int:
        rows = await self.connection.execute(
            "SELECT tfr_id FROM tfrs ORDER BY tfr_id DESC LIMIT 1"
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            tfr_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO tfrs(tfr_id, company_name, rocket_name, date, time_utc, area, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    tfr_id,
                    company_name,
                    rocket_name,
                    date,
                    time_utc,
                    area,
                    reason
                ),
            )
            await self.connection.commit()
            return tfr_id