import math


def calculate_drywall_materials(height, width):
  if height <= 0 or width <= 0:
    return None

  perimeter = (height * 2) + (width * 2)
  area = (height * width) * 2
  profile_length = 2.60

  # 1. Tracks: Floor + Ceiling (width * 2) / 2.60m profile length
  tracks = math.ceil((width * 2) / profile_length)

  # 2. Studs: Marks every 0.40m along the width plus the 0 mark
  base_studs_count = math.ceil(width / 0.40) + 1

  if height > profile_length:
    studs = math.ceil((base_studs_count * (height + 0.30)) / profile_length)
    t1_screws_splice = base_studs_count * 8
  else:
    studs = math.ceil(base_studs_count)
    t1_screws_splice = 0

  # 3. Boards: Double face, 2.88m2 per board (1.20x2.40)
  boards = math.ceil(area / 2.88)

  # 4. Anchors: Perimeter scaling (every ~0.37m)
  anchors = math.ceil(perimeter * 2.66)

  # 5. T1 Screws: Structure assembly + reinforcement for splices
  t1_screws = math.ceil(60 + t1_screws_splice)

  # 6. T2 Screws: Proportional to boards (~50 per board)
  t2_screws = math.ceil(boards * 50)

  # 7. Paper Tape: 1.32m per m2
  tape = round(area * 1.32, 2)

  # 8. Joint Compound: 0.60 kg per m2
  compound = round(area * 0.60, 2)

  return {
      "Total Area (m2)": round(area, 2),
      "Perimeter (m)": round(perimeter, 2),
      "Tracks": tracks,
      "Studs": studs,
      "Boards": boards,
      "Anchors": anchors,
      "T1 Screws": t1_screws,
      "T2 Screws": t2_screws,
      "Paper Tape (m)": tape,
      "Joint Compound (kg)": compound,
  }