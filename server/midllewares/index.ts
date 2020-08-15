import express, { Express } from 'express';
import helmet from 'helmet';
import morgan from 'morgan';
import cookieParser from 'cookie-parser';

import { manifestHelper } from './manifestHelper';
import { paths } from '../../config/paths';
// import { webpackDevServer } from './webpackDevServer';

const isDev = process.env.NODE_ENV === 'development';

export const middlewares = async (app: Express) => {
  // add secured http headers
  if (isDev) {
    app.use(
      helmet({
        contentSecurityPolicy: {
          directives: {
            'default-src': ["'self'", 'localhost:8051'],
          },
        },
      })
    );
  } else {
    app.use(helmet());
  }

  // log requests basic info
  app.use(morgan('dev'));

  // body parser
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  app.use(cookieParser());

  // handle static files via nginx server.
  if (isDev) {
    app.use(express.static(paths.buildWeb));
  }

  // help to read and parse manifest file to get assets paths.
  app.use(manifestHelper(`${paths.buildWeb}/manifest-app.json`));

  app.use((req, res, next) => {
    res.locals.meta = {
      defaultTitle: 'Mahmoud Ashraf',
      defaultDescription: "Mahmoud Ashraf's sapce on the internet.",
    };

    const { assetPath } = res.locals;

    const styles = [assetPath('app.css')];
    const scripts = [assetPath('app.js'), assetPath('vendor.js')];

    res.locals.styles = styles.filter(Boolean);
    res.locals.scripts = scripts.filter(Boolean);

    res.locals.cookies = req.cookies;

    next();
  });
};
