create table if not exists public.hanabi_checks (
  room text not null,
  item_key text not null,
  done boolean not null default false,
  updated_at timestamptz not null default now(),
  primary key (room, item_key)
);
alter table public.hanabi_checks enable row level security;
create policy "public read hanabi_checks" on public.hanabi_checks for select using (true);
create policy "public insert hanabi_checks" on public.hanabi_checks for insert with check (true);
create policy "public update hanabi_checks" on public.hanabi_checks for update using (true);
alter publication supabase_realtime add table public.hanabi_checks;
