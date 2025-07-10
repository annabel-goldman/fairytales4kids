describe('Story Pages', () => {
  const storyPages = [
    'cinderella',
    'snow-white',
    'sleeping-beauty',
    'rapunzel',
    'little-red-riding-hood',
    'jack-and-the-beanstalk',
    'three-little-pigs',
    'goldilocks',
    'hansel-and-gretel',
    'frog-prince'
  ]

  storyPages.forEach(story => {
    it(`should load ${story} story page`, () => {
      cy.visit(`/pages/stories/${story}.html`)
      
      // Check if page loads
      cy.get('body').should('be.visible')
      
      // Check for story content
      cy.get('h1, h2, h3').should('exist')
      cy.get('p').should('exist')
      
      // Check for navigation back to home
      cy.get('a[href*="index.html"], a[href="/"]').should('exist')
      
      // Check for images
      cy.get('img').should('exist')
    })
  })

  it('should have working navigation between stories', () => {
    cy.visit('/pages/stories/cinderella.html')
    
    // Check if there are links to other stories
    cy.get('a[href*=".html"]').should('exist')
    
    // Test clicking on a story link
    cy.get('a[href*="snow-white.html"]').first().click()
    cy.url().should('include', 'snow-white')
  })
}) 