import pandas as pd


def 정제(df):
    df = df.copy()
    print("시작       ", len(df))

    df = df.dropna(subset=["점수"])
    print("빈 칸 제거 ", len(df))

    df = df.drop_duplicates()
    print("중복 제거  ", len(df))

    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()

    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print("범위 밖 제거", len(df))

    return df


def 반별평균(df):
    return df.groupby("반")["점수"].mean().round(2)


if __name__ == "__main__":
    raw_df = pd.read_csv("scores_2026.csv")
    df = 정제(raw_df)

    math_df = df[df["과목"] == "수학"]
    print("\n[① 수학 과목 행 수]", len(math_df))

    high_1ban = df[(df["반"] == "1반") & (df["점수"] >= 90)]
    print("[응용: 1반 & 90점 이상 행 수]", len(high_1ban))

    class_mean = df.groupby("반")["점수"].mean().round(2)
    subject_class_mean = df.groupby(["과목", "반"])["점수"].mean().round(2)
    print("\n[②-1 반별 평균]\n", class_mean)
    print("\n[②-2 과목 x 반 평균]\n", subject_class_mean)

    class_stats = df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2)
    print("\n[③ 반별 통계 요약]\n", class_stats)

    print("\n[검증 ② 합계 일치]")
    print("그룹 합계의 합:", df.groupby("반")["점수"].sum().sum())
    print("전체 점수 합계:", df["점수"].sum())

    print("\n[검증 ② 개수 일치]")
    print("그룹 개수의 합:", df.groupby("반")["점수"].count().sum())
    print("전체 행 수(len):", len(df))

    spot = df[(df["반"] == "1반") & (df["과목"] == "수학")]["점수"]
    print("\n[검증 ④ 스팟 체크: 1반 수학 점수 목록]\n", spot.tolist())
    print("개수:", len(spot), "합계:", spot.sum(), "평균:", round(spot.mean(), 2))