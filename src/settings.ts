export const profile = {
	fullName: 'Abhishek Ajith',
	title: 'PhD Researcher in Regenerative Biomaterials',
	institute: 'Cochin University of Science and Technology (CUSAT)',
	author_name: 'Abhishek A', // Author name to be highlighted in the papers section
	research_areas: [
		{
			title: 'Regenerative Biomaterials',
			description:
				'Designing biodegradable, inherently radiopaque biomaterials for orthopaedic and craniomaxillofacial repair.',
			field: 'biology',
		},
		{
			title: 'Theranostics & Cancer Therapy',
			description:
				'Engineering imageable drug-eluting embolics for locoregional hepatocellular carcinoma therapy.',
			field: 'chemistry',
		},
		{
			title: 'Periodontal Regeneration',
			description:
				'Developing early-biomineralizing nanocellulose–brushite self-setting composites for periodontal repair.',
			field: 'engineering',
		},
	],
}

export const social = {
	email: 'mailtoabhishek97@gmail.com',
	linkedin: 'https://www.linkedin.com/in/abhishekajith/',
	x: '',
	bluesky: '',
	github: 'https://github.com/abhishekajith',
	gitlab: '',
	scholar: '',
	inspire: '',
	arxiv: '',
	orcid: 'https://orcid.org/0000-0002-8939-9948',
}

export const template = {
	website_url: 'https://abhishekajith.github.io', // Astro needs to know your site’s deployed URL to generate a sitemap. It must start with http:// or https://
	menu_left: false,
	transitions: true,
	lightTheme: 'light', // Select one of the Daisy UI Themes or create your own
	darkTheme: 'dark', // Select one of the Daisy UI Themes or create your own
	excerptLength: 200,
	postPerPage: 5,
    base: '' // Repository name starting with /
}

export const seo = {
	default_title: 'Abhishek Ajith - Regenerative Biomaterials',
	default_description:
		'PhD researcher designing inherently radiopaque, biodegradable biomaterials for orthopaedic repair and locoregional cancer therapy.',
	default_image: '/images/astro-academia.png',
}
