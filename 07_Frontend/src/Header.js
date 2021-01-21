import React from 'react';
import { AiFillGithub, AiFillFilePdf } from 'react-icons/ai';

const Header = () => {
  return (
    <div className="header-main">
      <a href="https://github.com/youurt/portfolio" className="links">
        <AiFillGithub /> Go to Project
      </a>{' '}
      <a href="Masterarbeit.pdf" className="links">
        <AiFillFilePdf /> Download Thesis
      </a>
      <div className="text">
        Das Modell wurde auf einem selbst erstellten Datensatz trainiert. Der
        Datensatz beinhaltet 20.000 Schlagzeilen, bestehend aus zwei Klassen.
        Das Modell wird vollständig im Browser ausgeführt und ist ca. 3 MB groß.
      </div>
    </div>
  );
};

export default Header;
