"""Fundo estilo oceano/ondas (inspirado no efeito wave CSS), adaptado ao Qt e às cores do tema."""

from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QBrush, QPainterPath, QRadialGradient


class OceanWaveRenderer:
    """Estado + pintura procedural de ondas; sem assets externos."""

    def __init__(self) -> None:
        self._phase = 0.0
        self._swell = 0.0

    def advance(self) -> None:
        # Velocidade calibrada para loop suave (~6–8s por sensação visual)
        self._phase += 0.078
        self._swell += 0.052

    def paint(
        self,
        painter: QPainter,
        rect: QRectF,
        background_hex: str,
        text_hex: str,
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing, True)
        w, h = rect.width(), rect.height()
        if w < 4 or h < 4:
            return

        bg = QColor(background_hex)
        if not bg.isValid():
            bg = QColor("#0c0e14")
        tc = QColor(text_hex)
        if not tc.isValid():
            tc = QColor("#ece8f4")

        is_dark = bg.lightness() < 140
        scale = max(0.55, min(w, h) / 520.0)

        # 1) Radial central (equivalente ao gradiente do body no CSS de referência)
        cx, cy = w * 0.5, h * 0.38
        radius = min(w, h) * 0.78
        rg = QRadialGradient(QPointF(cx, cy), radius)
        center_col = QColor(bg)
        if is_dark:
            center_col = center_col.lighter(108)
        else:
            center_col = center_col.lighter(103)
        edge_col = QColor(bg)
        if is_dark:
            edge_col = edge_col.darker(104)
        else:
            edge_col = edge_col.darker(102)
        rg.setColorAt(0.0, center_col)
        rg.setColorAt(0.45, QColor(bg))
        rg.setColorAt(1.0, edge_col)
        painter.fillRect(rect, QBrush(rg))

        # 2) Faixa inferior (“ocean”)
        ocean_frac = 0.17
        ocean_top = h * (1.0 - ocean_frac)
        ocean = QColor(bg)
        if is_dark:
            ocean = QColor(
                max(0, int(bg.red() * 0.42 + 8)),
                max(0, int(bg.green() * 0.62 + 22)),
                max(0, int(bg.blue() * 0.88 + 36)),
            ).darker(108)
        else:
            ocean = ocean.darker(107)

        painter.fillRect(QRectF(0, ocean_top, w, h - ocean_top), ocean)

        # 3) Duas ondas desfasadas + leve swell na segunda
        wavelength1 = max(130.0, w * 0.44)
        wavelength2 = max(110.0, w * 0.36)
        amp1 = 12.0 * scale
        amp2 = 8.5 * scale
        scroll1 = (self._phase * 36.0) % (wavelength1 * 2)
        scroll2 = (self._phase * 40.0 + wavelength2 * 0.18) % (wavelength2 * 2)
        swell = 5.5 * scale * math.sin(self._swell)

        def wave_path(phase_px: float, amp: float, base_y: float, wavelength: float, swell_y: float) -> QPainterPath:
            path = QPainterPath()
            path.moveTo(0, h)
            step = max(3, int(5 * scale))
            xs = list(range(0, int(w) + 1, step))
            if not xs or xs[-1] < int(w):
                xs.append(int(w))
            for x in xs:
                ang = (x - phase_px) * (2 * math.pi / wavelength)
                y = base_y + swell_y + amp * math.sin(ang)
                path.lineTo(x, y)
            path.lineTo(w, h)
            path.closeSubpath()
            return path

        base_y1 = ocean_top - 1.0 * scale
        base_y2 = ocean_top + 5.0 * scale

        if is_dark:
            foam1 = QColor(bg.lighter(128))
            foam1.setAlpha(58)
            foam2 = QColor(bg.lighter(118))
            foam2.setAlpha(38)
        else:
            foam1 = QColor(255, 255, 255, 48)
            foam2 = QColor(tc)
            foam2.setAlpha(28)

        path1 = wave_path(scroll1, amp1, base_y1, wavelength1, 0.0)
        painter.fillPath(path1, QBrush(foam1))

        path2 = wave_path(scroll2, amp2, base_y2, wavelength2, swell * 0.9)
        painter.fillPath(path2, QBrush(foam2))
