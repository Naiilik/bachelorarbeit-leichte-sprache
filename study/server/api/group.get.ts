import { groups } from "../../app/groups";

export default defineEventHandler(async (event) => {
  const db = event.context.cloudflare.env.DB;

  // Fehlende Gruppen automatisch anlegen
  for (const group of groups) {
    await db
      .prepare(`INSERT OR IGNORE INTO assignment_counter (group_name, count) VALUES (?, 0)`)
      .bind(group)
      .run();
  }

  // Gruppe mit dem niedrigsten Zähler ermitteln (nur lesen, nicht inkrementieren)
  const placeholders = groups.map(() => "?").join(", ");
  const row = await db
    .prepare(`SELECT group_name FROM assignment_counter WHERE group_name IN (${placeholders}) ORDER BY count ASC LIMIT 1`)
    .bind(...groups)
    .first() as { group_name: string } | null;

  if (!row) throw createError({ statusCode: 500, message: "Keine Gruppen gefunden." });

  return { group: row.group_name };
});
