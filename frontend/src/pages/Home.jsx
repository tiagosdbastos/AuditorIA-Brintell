import { useState } from "react";
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

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/analisar-edital/",
      // const response = await fetch(
      //   "https://auditoria-brintell.onrender.com/analisar-edital/",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ocorreu um erro no servidor.");
      }

      const data = await response.json();

      onReportGenerated(data);
    } catch (error) {
      console.error("Erro ao chamar API:", error);
      alert(`Erro: ${error.message}`);
    } finally {
      setLoading(false);
    }
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
