export default defineEventHandler(async (event) => {
  const body = await readBody(event);

  const db = event.context.cloudflare.env.DB;

  await db
    .prepare(
      `
      INSERT INTO results (
        participant_id,
        group_name,
        score,
        answers
      )
      VALUES (?, ?, ?, ?)
    `,
    )
    .bind(
      crypto.randomUUID(),
      body.group,
      body.score,
      JSON.stringify(body.answers),
    )
    .run();

  // Zähler der Gruppe nach erfolgreicher Abgabe erhöhen
  await db
    .prepare(`UPDATE assignment_counter SET count = count + 1 WHERE group_name = ?`)
    .bind(body.group)
    .run();

  return {
    success: true,
  };
});
