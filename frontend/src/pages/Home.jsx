import React, { useState } from "react";
import UploadArea from "../components/UploadArea";

export default function Home({ onReportGenerated }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!file) {
      alert("Por favor, selecione um arquivo PDF antes de continuar.");
      return;
    }
    setLoading(true);

    setTimeout(() => {
      const fakeReport = {
        resumo: {
          objeto: "Aquisição de materiais de informática",
          modalidade: "Pregão Eletrônico",
          valor: "R$ 250.000,00",
        },
        riscos: [
          "Exigência excessiva de atestados técnicos",
          "Prazo de entrega inferior a 5 dias úteis",
        ],
        legislacao: [
          "Lei nº 14.133/2021 — Nova Lei de Licitações",
          "Decreto nº 10.024/2019 — Pregão Eletrônico",
        ],
        jurisprudencia: [
          "Acórdão 1234/2023 - TCE/SP — Prazos exíguos violam a isonomia",
          "Decisão 456/2022 - TCU — Restrições técnicas desproporcionais",
        ],
        conclusao:
          "O edital apresenta cláusulas potencialmente restritivas e deve ser revisado antes da publicação.",
      };
      setLoading(false);
      onReportGenerated(fakeReport);
    }, 1800);
  };

  return (
    <section className="home">
      <h1>Análise Inteligente de Editais</h1>
      <p>
        Faça upload de um edital em PDF para que o Auditor-IA gere um relatório
        automático com resumo, riscos e legislação aplicável.
      </p>

      <UploadArea onFileSelected={setFile} />

      <div className="controls">
        <button
          className="btn primary"
          disabled={!file || loading}
          onClick={handleAnalyze}
        >
          {loading ? "Analisando..." : "Analisar Edital"}
        </button>
      </div>
    </section>
  );
}
