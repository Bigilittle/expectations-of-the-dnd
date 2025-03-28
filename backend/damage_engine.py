from typing import Dict

def combine_with_crit(
    base_dist: Dict[int, float],
    crit_dist: Dict[int, float],
    p_total_hit: float,
    p_crit: float = 0.05
) -> Dict[int, float]:
    """
    Комбинирует обычное и критическое распределения урона с учётом вероятности попадания и крита.

    :param base_dist: Распределение обычного урона {урон: вероятность}
    :param crit_dist: Распределение урона при крите
    :param p_total_hit: Общая вероятность попадания (включая крит)
    :param p_crit: Вероятность крита (по умолчанию 5%)
    :return: Финальное распределение урона
    """
    p_hit_regular = max(p_total_hit - p_crit, 0)
    p_miss = max(0.05, 1.0 - p_hit_regular - p_crit)

    final_dist: Dict[int, float] = {}

    # обычное попадание
    for dmg, prob in base_dist.items():
        final_dist[dmg] = final_dist.get(dmg, 0) + prob * p_hit_regular

    # критическое попадание
    for dmg, prob in crit_dist.items():
        final_dist[dmg] = final_dist.get(dmg, 0) + prob * p_crit

    # промах
    final_dist[0] = final_dist.get(0, 0) + p_miss

    return final_dist